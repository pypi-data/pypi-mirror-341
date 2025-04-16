import numpy as np
from scipy.ndimage import labeled_comprehension

def get_cell_expression_fast(multi_channel_image, segmentation_masks):
    
    unique_cells = np.unique(segmentation_masks)
    unique_cells = unique_cells[unique_cells > 0]  # Exclude background (label 0)

    print(multi_channel_image.shape, segmentation_masks.shape)

    expressions = []
    for image in multi_channel_image:
    # Compute mean expression per channel efficiently
        expr = labeled_comprehension(
            image,  # Multi-channel image
            segmentation_masks,   # Labels
            unique_cells,         # Unique cell IDs
            np.mean, 
            out_dtype=np.float32, # Function to apply
            default=0             # Default value for empty regions
        )
        
        expressions.append(expr)
        
    return np.array(expressions)