# Imports
import os
import warnings
from pathlib import Path

# External imports
import tifffile
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Package imports
from numbers_and_brightness.defaults import (
    DEFAULT_BACKGROUND,
    DEFAULT_SEGMENT,
    DEFAULT_DIAMETER,
    DEFAULT_FLOW_THRESHOLD,
    DEFAULT_CELLPROB_THRESHOLD,
    DEFAULT_ANALYSIS,
    DEFAULT_ERODE
)

def _load_model():
    print("Loading cellpose...")
    from cellpose import models
    from torch.cuda import is_available
    if is_available():
        gpu=True
        print("Using cuda GPU")
    else:
        gpu=False
        print("Using CPU")
    print("Loading model...")
    model = models.Cellpose(gpu=gpu, model_type='cyto3')
    return model

def _segment(original_img, outputdir, model, diameter, flow_threshold, cellprob_threshold):
    if model == None:
        model=_load_model()

    max_proj = np.max(original_img, axis=0)
    mask, flow, styles, diams = model.eval(max_proj, diameter=diameter, flow_threshold=flow_threshold, cellprob_threshold=cellprob_threshold)

    # Save mask
    np.save(os.path.join(outputdir, "cellmask.npy"), mask)

    # Save mask visualisation
    from cellpose import utils
    plt.imshow(max_proj, cmap='gray')
    outlines = utils.outlines_list(mask)
    for o in outlines:
        plt.plot(o[:,0], o[:,1], color='r')
    plt.axis('off')
    plt.colorbar()
    plt.title("cellmask")
    plt.savefig(os.path.join(outputdir, "cellmask.png"))
    plt.close()

    return mask

def _analysis(img, outputdir, mask, brightness, intensity, erode):
    if len(np.unique(mask))<2: return    # If no cells detected, do not perform analysis
    
    if erode > 0:
        from cellpose import utils
        import cv2
        from scipy.stats import gaussian_kde

        plt.imshow(np.max(img, axis=0), cmap='gray')
        outlines = utils.outlines_list(mask)
        for o in outlines:
            plt.plot(o[:,0], o[:,1], color='r')

        shrunk_masks = np.zeros(shape=(img.shape[1], img.shape[2]))

        kernel_size = erode
        kernel = np.ones((kernel_size*2, kernel_size*2), np.uint8)

        for cell in np.unique(mask[mask!=0]):
            cell_mask = mask==cell
            cell_mask_uint8 = cell_mask.astype(np.uint8)
            shrunk_mask = cv2.erode(cell_mask_uint8, kernel)
            shrunk_mask = shrunk_mask.astype(np.bool)

            outlines = utils.outlines_list(shrunk_mask)
            for o in outlines:
                plt.plot(o[:,0], o[:,1], color='green')
            shrunk_masks[shrunk_mask]=cell

        mask = shrunk_masks

        plt.axis('off')
        plt.colorbar()
        plt.title('eroded mask')
        plt.savefig(os.path.join(outputdir, "eroded_mask.png"))
        plt.close()

    # Show mask on brightness
    plt.imshow(brightness, cmap='plasma')
    outlines = utils.outlines_list(mask)
    for o in outlines:
        plt.plot(o[:,0], o[:,1], color='r')
    plt.axis('off')
    plt.colorbar()
    plt.title('mask on brightness')
    plt.savefig(os.path.join(outputdir, "mask_on_brightness.png"))
    plt.close()

    mask[mask>0] = 1    # Convert all cells in mask to 'True'
    mask = mask.astype(np.bool)

    brightness_cell = brightness[mask]
    brightness_flat = brightness_cell.flatten()
    intensity_cell = intensity[mask]
    intensity_flat = intensity_cell.flatten()

    x = np.nan_to_num(brightness_flat, copy=True, nan=0.0, posinf=0.0, neginf=0.0)
    y = np.nan_to_num(intensity_flat, copy=True, nan=0.0, posinf=0.0, neginf=0.0)
    xy = np.vstack([x, y])
    z = gaussian_kde(xy)(xy)

    plt.scatter(intensity_flat, brightness_flat, c=z, s=1, cmap='hsv_r')
    plt.title("Intensity x Brightness")
    plt.xlabel('Intensity')
    plt.ylabel('Brightness')
    plt.savefig(os.path.join(outputdir, "brightness_x_intensity.png"))

def numbers_and_brightness_analysis(file: str,
                                    model=None,
                                    background=DEFAULT_BACKGROUND,
                                    segment=DEFAULT_SEGMENT,
                                    diameter=DEFAULT_DIAMETER,
                                    flow_threshold=DEFAULT_FLOW_THRESHOLD,
                                    cellprob_threshold=DEFAULT_CELLPROB_THRESHOLD,
                                    analysis=DEFAULT_ANALYSIS,
                                    erode=DEFAULT_ERODE
                                    ):
    file=Path(file)
    if analysis: segment = True     # Segmentation is needed for analysis

    img = tifffile.imread(file)

    # Create new directory
    outputdir = f"{os.path.splitext(file)[0]}_n_and_b_output"
    if not os.path.isdir(outputdir): os.mkdir(outputdir)

    average_intensity = np.mean(img, axis=0)
    variance = np.var(img, axis=0)
    
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)  # Ignore 'division by zero' or 'invalid value encountered in divide' warnings caused by x/0 or 0/0
        apparent_brightness = variance / average_intensity
        apparent_number = average_intensity**2 / variance

        brightness = (variance - average_intensity) / (average_intensity - background)
        number = ((average_intensity-background)**2) / np.clip((variance - average_intensity), 1e-6, None)

    # For all imgs, save matplotlib image and tiffile
    arrays = [average_intensity, variance, apparent_brightness, apparent_number, brightness, number]
    names = ["intensity", "variance", "apparent_brightness", "apparent_number", "brightness", "number"]
    for i, arr in enumerate(arrays):
        # Save tifffile
        tifffile.imwrite(os.path.join(outputdir, f"{names[i]}.tif"), arr)

        # Create and save matplotlib image
        plt.imshow(arr, cmap='plasma')
        plt.axis('off')
        plt.colorbar()
        plt.title(names[i])
        plt.savefig(os.path.join(outputdir, f"{names[i]}.png"))
        plt.close()

    # Perform segmentation using cellpose
    if segment:
        mask = _segment(original_img=img, model=model, diameter=diameter, flow_threshold=flow_threshold, cellprob_threshold=cellprob_threshold, outputdir=outputdir)

    if analysis:
        _analysis(img=img, outputdir=outputdir, mask=mask, brightness=apparent_brightness, intensity=average_intensity, erode=erode)

def numbers_and_brightness_batch(folder,
                                 background=DEFAULT_BACKGROUND,
                                 segment=DEFAULT_SEGMENT,
                                 diameter=DEFAULT_DIAMETER,
                                 flow_threshold=DEFAULT_FLOW_THRESHOLD,
                                 cellprob_threshold=DEFAULT_CELLPROB_THRESHOLD,
                                 analysis=DEFAULT_ANALYSIS,
                                 erode=DEFAULT_ERODE
                                 ):
    folder = Path(folder)

    if analysis: segment = True     # Segmentation is needed for analysis

    # Collect all tiff files in folder
    extensions = ['.tif', '.tiff']
    files = [f for f in folder.iterdir() if f.suffix.lower() in extensions]

    # Initialize model if user wants automatic segmentation
    model = _load_model() if segment else None

    # Process all files
    for file in tqdm(files):
        numbers_and_brightness_analysis(file=file, analysis=analysis, erode=erode, background=background, segment=segment, diameter=diameter, flow_threshold=flow_threshold, cellprob_threshold=cellprob_threshold, model=model)