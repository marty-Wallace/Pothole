# Pothole
A set of python scripts and a Rust binary application for detecting potholes and road cracks. 

![putpixel](https://github.com/marty-Wallace/Pothole/blob/master/images/road/road_blur35_floodfill_1.png)

### Python
To run the python scripts simply run `python pothole.py --help`

The required inputs for the script are the input file(which must be a space seperated ascii file for now), the output filename and the various algorithms you want to run on them. 

##### An example
```
python pothole.py --input=data/reclas_fixed.txt --output=data/output.txt --alg=blur,floodfill --blurfilter=Simple35 --growth=25 --progress
```

In this case the input file is specified as data/reclas_fixed.txt the output file will be data/output.txt the algorithms applied in order will be blur then floodfill. The blur filter will be a Simple35 and the floodfill with use a growth factor of 25. The `--progress` flag tells the script to display console progress bars to show it's progress.
 
##### Another example
```
python pothole.py --input=data/reclas_fixed.txt --output=images/output_image.png --alg=floodfill --image --growth=10
```

In this case the input file will be the same but the output file will be named images/output_image.png. The `--image` flag tells the script to save it as an image rather than an ascii file. 



### Rust 

You will need the Rust compiler to run this code. Installation instructions can be found at https://www.rust-lang.org/en-US/install.html if you wish to run it. 

##### To Run
```
cd pothole
cargo build --release 
cargo run --release --help
```
##### An example
```
cargo run --input=../data/reclas_fixed.txt --ouput=../images/output.png --alg=floodsame,floodfill --image --verbose --growth=120 --sizemin=20 --samegrowth=40
```

In this example the `--input` option specifies that the input file is data/reclas_fixed.txt, the `--output` option specifies the output file is images/output.png. The `--algs` specifies the algorithms to be executed in order are floodsame then floodfill. `--image` means it will save as an image rather than a text file. `--verbose` flag means it will print out what it's doing. `--growth` affects the growth factor of the floodfill algorithm. The `--samegrowth` affects the growth factor of the floodsame algorithm and the `--sizemin` value indicates the largest group size to ignore while executing the floodsame algorithm. 

##### One more example 
```
cargo run --input=../data/reclas_fixed.txt --ouput=../data/output.txt --alg=blur,floodfill --roadvalue=2 --blursize=3 --truncate
```
In this example the output file is a text file rather than an image. The algorithms are executed in the order blur -> floodfill. `--roadvalue` indicates the value of the road in the input file (in the reclas file it is 127 so the script defaults to 127). The `blursize=3` means it will execute its blur on 3x3 squares and the `--truncate` flag means it will truncate division on blurs (this can have some wacky effects). 
