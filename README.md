# Goal 
To create a model that can classify and 'read' pictures of pre-Islamic North Arabian inscriptions of different script types.

## Sub-goals
- Create a model that can classify inscriptions based on script type (ex. Safaitic vs. Nabataean)
- Create a model that can OCR inscriptions
- Create a model that can 'translate' inscriptions

## Obstacles and Limitations
- The data will be retrieved from [Ociana](https://ociana.osu.edu/)
- Ociana has images of many different script types. But it only has sufficient data for the **Safaitic** script type. Hence, The classification model will only be able to tell between **Safaitic** and **Non-Safaitic**
- I noticed two different types of images in Ociana database, original images (taken via a camera by any passer-by), or traced out images, which are the black inscription tracing on a white background. Traced images are much cleaner than original images. Original images may be blurry and unclear due to lack of care while taking the picture. Hence, the models will be trained using traced images to start.

## Next Steps
- Gather the data to create the classification model. Should have 2 folders: **safaitic** and **other**.

## Miscellaneous
- Models are createad in Jupyter notebook files. Install requirements and run `jupyter lab` to open them.
