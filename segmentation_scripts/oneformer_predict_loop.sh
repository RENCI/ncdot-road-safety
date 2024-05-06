#!/bin/bash

start=$(date)
for ((n = $2; n < $3; n++)); do
    DIVISION=$1
    SUBDIR=$n
    FILES=(/projects/ncdot/NC_2018_Secondary/${DIVISION}/${SUBDIR}/**/*.jpg)
    OUT_DIR=/projects/ncdot/NC_2018_Secondary_2/segmentations/${DIVISION}/${SUBDIR}
    mkdir $OUT_DIR

    for (( i = 0; i < "${#FILES[@]}"; i += 2000)); do
        for f in "${FILES[@]:i:2000}"; do
            FNAME=$OUT_DIR/$(basename $f)

            if [[ ! -e "${FNAME%.jpg}.png" && ! "${FNAME}" =~ 6.jpg$ ]];
            then
                cp $f $OUT_DIR/$(basename $f)
            fi
        done

        python resize_images_ratio.py -d $OUT_DIR -o $OUT_DIR -H 512

        python OneFormer/demo/oneformer_predict_batch_hatteras.py --input_directory $OUT_DIR --batch 16 --output $OUT_DIR --model mapillary_convnext_xl

        rm $OUT_DIR/*.jpg
    done
    echo "Done with ${OUT_DIR}"
done
end=$(date)
echo "Start Time: ${start}"
echo "End Time: ${end}"
