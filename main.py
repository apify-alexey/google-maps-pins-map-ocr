import cv2 as cv
import numpy as np
import os, json
import base64

from apify_client import ApifyClient

# Run the main function of the script, if the script is executed directly
if __name__ == '__main__':
    # Initialize the main ApifyClient instance
    client = ApifyClient(os.environ['APIFY_TOKEN'], api_url=os.environ['APIFY_API_BASE_URL'])

    # Get the resource subclient for working with the default key-value store of the actor
    default_kv_store_client = client.key_value_store(os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID'])

    # Get the value of the actor input and print it
    actor_input = default_kv_store_client.get_record(os.environ['APIFY_INPUT_KEY'])['value']

    # Get the resource subclient for working with the default dataset of the actor
    default_dataset_client = client.dataset(os.environ['APIFY_DEFAULT_DATASET_ID'])

    base64_decoded = base64.b64decode(actor_input['base64Image'].replace('data:image/png;base64,', '', 1))

    # TODO actor not supposed to be run from Apify Cloud UI, however if needed shortcut to local file
    # might be quick changed to create file from external source like file URL or Apify file uploader
    with open("out.png", "wb") as out_file:
        out_file.write(base64_decoded)

    alpha = 2.5
    beta = -2.5*128 + 50
    threshold = 0.65
    distance = 10
    with open('out.png', 'rb') as f:
        img_data = np.asarray(bytearray(f.read()), dtype=np.uint8)
        img_color = cv.imdecode(img_data, 1)

        print(f"Image loaded, size {len(img_data)}")
        print(f"Map shape: {img_color.shape[:2]}")

        img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
        img_boosted = cv.convertScaleAbs(img_gray, alpha=alpha, beta=beta)

        print("Phase 1/3 (boosting) finished...")

        print("Loading pin and matching...")
        pinfile = os.path.dirname(os.path.realpath(__file__)) + "/pin.png"
        template = cv.imread(pinfile,0)
        w, h = template.shape[::-1]

        res = cv.matchTemplate(img_boosted,template,cv.TM_CCOEFF_NORMED)

        print("Phase 2/3 (lookup) finished...")
        print("Deduplicating matches...")

        loc = zip(*np.where(res >= threshold)[::-1])

        dedup = []
        for pt in loc:
            if(len([x for x in dedup if abs(x['x'] - pt[0]) < distance and abs(x['y'] - pt[1]) < distance]) == 0):
                dedup.append({'x': int(pt[0]), 'y': int(pt[1])})

        print("Phase 3/3 (deduplication) finished...")
        print(f"Found {len(dedup)} unique pins...")

        print(json.dumps({
            "Points found": len(dedup)
        }))

        # Save points
        default_dataset_client.push_items(dedup)
        default_kv_store_client.set_record('OUTPUT', dedup)
