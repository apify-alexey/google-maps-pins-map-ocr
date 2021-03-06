# OCR for google map pins

## Input

Input must be `base64Image` string of `data:image/png;base64` content, visual data expected to be tiled google map as illustrated by `sample.png`
Input image saved as `inputImage.png` in KV store before processing, in order to disable saving image set `saveImage` to `false`

<p align="center">
<a href="https://raw.githubusercontent.com/apify-alexey/google-maps-pins-map-ocr/main/sample.png" target="_blank" rel="noopener noreferrer" onclick="window.open(this.href,'_blank');return false;"><img src="https://raw.githubusercontent.com/apify-alexey/google-maps-pins-map-ocr/main/sample.png" alt="" style="width: 320px; height: 240px;" width="320" height="240" /></a>
</p>

If image data is not valid (wrong encoding, format or content) then actor will fail.

Example of the input with actual content replaced by `[BASE64DATA_STAND_IN]`

```json
{
  "base64Image": "data:image/png;base64,[BASE64DATA_STAND_IN]",
  "saveImage": true
}
```

To quick validate input data please use [Base64 Image Viewer](https://jaredwinick.github.io/base64-image-viewer/) or similar tools.

## Output

Actor will try to find pins specified exactly by sprite `pin.png` and store coordinates of the pins found in dataset and `OUTPUT` as follows:

```json
[{
  "x": 10,
  "y": 1
},
{
  "x": 1602,
  "y": 15
},
{
  "x": 1849,
  "y": 31
}]
```
