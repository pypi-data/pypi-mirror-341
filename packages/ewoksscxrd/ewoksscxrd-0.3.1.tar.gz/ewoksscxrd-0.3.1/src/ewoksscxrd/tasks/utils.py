import io
import os
from cryio import crysalis
import h5py
import numpy as np
import concurrent.futures
import types
from fabio.limaimage import LimaImage
import hdf5plugin
from fabio import nexus


def create_run_file(scans, crysalis_dir, basename):
    """
    Create a Crysalis run file using the provided scans.
    """
    runHeader = crysalis.RunHeader(basename.encode(), crysalis_dir.encode(), 1)
    runname = os.path.join(crysalis_dir, basename)
    runFile = []
    # Expecting scans to be a list of lists; process the first set of scans.
    for omega_run in scans[0]:
        dscr = crysalis.RunDscr(0)
        dscr.axis = crysalis.SCAN_AXIS["OMEGA"]
        dscr.kappa = omega_run["kappa"]
        dscr.omegaphi = 0
        dscr.start = omega_run["omega_start"]
        dscr.end = omega_run["omega_end"]
        dscr.width = omega_run["domega"]
        dscr.todo = dscr.done = omega_run["count"]
        dscr.exposure = 1
        runFile.append(dscr)
    crysalis.saveRun(runname, runHeader, runFile)
    crysalis.saveCrysalisExpSettings(crysalis_dir)


def create_par_file(par_file, processed_data_dir, basename):
    """
    Create a new .par file using the contents of the original.
    Changes any "FILE CHIP" line so that the referenced file ends with '.ccd'.
    """
    new_par = os.path.join(processed_data_dir, basename)
    with io.open(new_par, "w", encoding="iso-8859-1") as new_file:
        with io.open(par_file, "r", encoding="iso-8859-1") as old_file:
            for line in old_file:
                if line.startswith("FILE CHIP"):
                    new_file.write(f"FILE CHIP {basename.replace('.par', '.ccd')} \n")
                else:
                    new_file.write(line)


def read_dataset(file_path):
    """Read dataset from '/entry_0000/measurement/data'."""
    with h5py.File(file_path, "r") as f:
        data = f["/entry_0000/measurement/data"][()]
    return data


def subtract_frame_inplace(frame, scale_factor, dectris_masking_value):
    """
    For each pixel in a frame:
      - If the pixel value in image1 exceeds dectris_masking_value,
        the corresponding pixel in frame[0] is set to image0 + image1.
      - Otherwise, frame[0] is set to image0 - image1.
    Afterwards, any negative values are clipped to 0.
    The operation is performed in-place on frame[0].

    Note: The 'scale_factor' parameter is retained for interface consistency
          but is not applied in this modified subtraction branch.
    """
    # Compute the subtracted result
    result = frame[0] - scale_factor * frame[1]

    # Create a boolean mask for pixels where image1 exceeds the threshold
    mask = frame[1] > dectris_masking_value

    # Use boolean indexing to apply the summed operation where the mask is True
    result[mask] = (2**32) - 1

    # Ensure no negative values remain by clipping at 0
    result[result < 0] = 0

    # Update the first image in-place
    frame[0][:] = result


def subtract_images_inplace_parallel(data, scale_factor, masking_value):
    """
    Processes a 4D dataset in parallel:
      - The input 'data' must have shape (nframes, 2, H, W).
      - Each frame is processed by subtract_frame_inplace with the given scale and threshold.
      - After processing, only image0 is returned as a 3D array.
    """
    if data.ndim != 4:
        raise ValueError("Input data must be 4D.")
    if data.shape[1] < 2:
        raise ValueError("Need at least 2 images along dimension 1.")
    num_frames = data.shape[0]
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        futures = [
            executor.submit(
                subtract_frame_inplace, data[i], scale_factor, masking_value
            )
            for i in range(num_frames)
        ]
        concurrent.futures.wait(futures)

    # Extract the first image across all frames
    result = data[:, 0, :, :]

    # If only one frame is present, remove the frame axis
    if result.shape[0] == 1:
        result = result[0]
    # Squeeze extra dimensions if needed
    if result.ndim != 3:
        result = np.squeeze(result)
    return result


def write_lima_images(result, output_path):
    """
    Write the result (assumed to be a 3D array (nframes, H, W)) as a LImA HDF5 image
    using a custom chunk size.
    """
    img = LimaImage(data=result)

    def custom_write(self, filename):
        start_time = nexus.get_isotime()
        abs_name = os.path.abspath(filename)
        mode = "a" if os.path.exists(abs_name) else "w"
        if hdf5plugin is None:
            compression = {"compression": "gzip", "compression_opts": 1}
        else:
            compression = hdf5plugin.Bitshuffle()
        with nexus.Nexus(abs_name, mode=mode, creator="LIMA-1.9.7") as nxs:
            entry = nxs.new_entry(
                entry="entry",
                program_name=None,
                title="Lima 2D detector acquisition",
                force_time=start_time,
                force_name=False,
            )
            measurement_grp = nxs.new_class(
                entry, "measurement", class_type="NXcollection"
            )
            instrument_grp = nxs.new_class(
                entry, "instrument", class_type="NXinstrument"
            )
            detector_grp = nxs.new_class(
                instrument_grp,
                self.header.get("detector", "detector"),
                class_type="NXdetector",
            )
            acq_grp = nxs.new_class(
                detector_grp, "acquisition", class_type="NXcollection"
            )
            info_grp = nxs.new_class(
                detector_grp, "detector_information", class_type="NXcollection"
            )
            info_grp["image_lima_type"] = f"Bpp{8 * int(self.dtype.itemsize)}"
            # self.data is assumed to be 3D: (nframes, H, W)
            nframes, H, W = self.data.shape
            max_bytes = 4 * 1024**3
            itemsize = self.dtype.itemsize
            max_rows = max(1, int(max_bytes // (itemsize * W)))
            new_chunk_rows = min(H, max_rows)
            max_grp = nxs.new_class(
                info_grp, "max_image_size", class_type="NXcollection"
            )
            max_grp["xsize"] = int(W)
            max_grp["ysize"] = int(H)
            header_grp = nxs.new_class(
                detector_grp, "header", class_type="NXcollection"
            )
            header_grp["acq_nb_frames"] = str(nframes)
            header_grp["image_bin"] = "<1x1>"
            header_grp["image_flip"] = "<flip x : False,flip y : False>"
            header_grp["image_roi"] = f"<0,0>-<{H}x{W}>"
            header_grp["image_rotation"] = "Rotation_0"
            op_grp = nxs.new_class(
                detector_grp, "image_operation", class_type="NXcollection"
            )
            op_grp["rotation"] = "Rotation_0"
            bin_grp = nxs.new_class(op_grp, "binning", class_type="NXcollection")
            bin_grp["x"] = 1
            bin_grp["y"] = 1
            dim_grp = nxs.new_class(op_grp, "dimension", class_type="NXcollection")
            dim_grp["xsize"] = int(W)
            dim_grp["ysize"] = int(H)
            flp_grp = nxs.new_class(op_grp, "flipping", class_type="NXcollection")
            flp_grp["x"] = 0
            flp_grp["y"] = 0
            roi_grp = nxs.new_class(
                op_grp, "region_of_interest", class_type="NXcollection"
            )
            roi_grp["xsize"] = int(W)
            roi_grp["ysize"] = int(H)
            roi_grp["xstart"] = 0
            roi_grp["ystart"] = 0
            plot_grp = nxs.new_class(detector_grp, "plot", class_type="NXdata")
            acq_grp["nb_frames"] = int(nframes)
            shape = (nframes, H, W)
            dataset = detector_grp.create_dataset(
                "data",
                shape=shape,
                chunks=(1, new_chunk_rows, W),
                dtype=self.dtype,
                **compression,
            )
            dataset.attrs["interpretation"] = "image"
            plot_grp["data"] = dataset
            plot_grp.attrs["signal"] = "data"
            measurement_grp["data"] = dataset
            for i in range(nframes):
                dataset[i] = self.data[i]
            entry.attrs["default"] = plot_grp.name

    img.write = types.MethodType(custom_write, img)
    img.write(output_path)
