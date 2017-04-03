extern crate rayon; 
extern crate raster;

#[macro_use]
extern crate clap;

use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;
use std::collections::HashMap;

use rayon::prelude::*;
use raster::{Image, Color};


fn main() {

    // command line arguments setup 
    let matches = 
        clap_app!(
         pothole =>
          (version: "1.0")
          (author: "Martin Wallace <martin.v.wallace@ieee.org>")
          (about: "Simple image processing to detect potholes")
          (@arg INPUT:      -i --input      +takes_value +required "Input file")
          (@arg OUTPUT:     -o --output     +takes_value +required "Output file")
          (@arg ALGORITHMS: -a --alg        +takes_value           "Comma seperated list of algorithms to apply")
          (@arg BLURSIZE:   -b --blursize   +takes_value           "The size of the blur to apply")
          (@arg GROWTH:     -g --growth     +takes_value           "The growth limit on a floodfill")
          (@arg COLORSTYLE: -c --colorstyle +takes_value           "Sets the blur mode to truncate rather than round")
          (@arg ROADVALUE:  -r --roadvalue  +takes_value           "Sets the number representing the road in the input file")
          (@arg IMAGE:      -m --image                             "Change output from .txt to an image")
          (@arg TRUNCATE:   -t --truncate                          "Sets the blur mode to truncate rather than round")
          (@arg VERBOSE:    -v --verbose                           "Display output while processing")
         )
        .get_matches();

    let mut blur_size  = 17_usize;
    let mut growth     = 1_i32;
    let mut colorstyle = "ColorWheel";
    let mut road_value = 2;

    // parse command line args 

    // set required options 
    let input_filename  = matches.value_of("INPUT").expect("Failed to unwrap input_filename");
    let output_filename = matches.value_of("OUTPUT").expect("Failed to unwrap output_filename");
    let algorithms      = matches.value_of("ALGORITHMS").expect("Failed to unwrap algorithm");

    // set optional options if they exists
    if matches.is_present("BLURSIZE") {
        blur_size = matches.value_of("BLURSIZE")
            .expect("Failed to unwrap blur size")
            .parse()
            .expect("Blur size must be an integer");
        if blur_size % 2 == 0 {
            panic!("Blur size must be an odd number");
        }
    }
    if matches.is_present("GROWTH") {
        growth = matches.value_of("GROWTH")
            .expect("Failed to unwrap growth")
            .parse()
            .expect("Growth must be an integer");
    }
    if matches.is_present("COLORSTYLE") {
        colorstyle = matches.value_of("COLORSTYLE")
            .expect("Failed to unwrap colorstyle")
    }
    if matches.is_present("ROADVALUE") {
        road_value = matches.value_of("ROADVALUE")
            .expect("Failed to unwrap roadvalue")
            .parse()
            .expect("roadvalue must be an integer");
    }
    
    // set flags 
    let image   = matches.is_present("IMAGE");
    let round   = !matches.is_present("TRUNCATE");
    let verbose = matches.is_present("VERBOSE");

    // Set input file for reading
    let input_file = File::open(input_filename.clone())
        .expect(& format!("Unable to open file {}", input_filename.clone()));
    let file = BufReader::new(&input_file);


    // read data from input file
    let mut im: Vec<Vec<u32>> = 
        file.lines()
        .map(|line| {
            line.unwrap()
                .split_whitespace()
                .map(|x| x.parse().expect("Error parsing integers in input file"))
                .collect()
        })
    .collect();

    // apply algorithms in order
    for alg in algorithms.split(",") {
        if verbose  {
            println!("Executing {}...\n", alg);
        }
        match alg {
            "blur" => {
                im = do_blur(&im, blur_size, round);
            },
            "floodfill" => {
                simple_floodfill(&mut im, growth, road_value);
            },
            "edges" => {
                unimplemented!();
            },
            "None" => {},
            _ => {
                panic!("Error algorithm {} is not recognized", alg);
            }
        }
    }

    //save data as image or as text file
    if verbose {
        println!("Saving data into {}...\n", output_filename);
    }
    if image {
        save_as_image(&im, output_filename, colorstyle);
    }else{
        save_as_textfile(&im, output_filename);

    }
}

fn do_blur(im: &Vec<Vec<u32>>, blur_size: usize, round: bool) -> Vec<Vec<u32>> {

    let size = im[0].len();
    // collect blurred image from parallel iterators

    (0..im.len())
        .into_par_iter()
        .map(|i| simple_blur(&im, i as usize, size, blur_size, round))
        .collect()
}

fn simple_blur(im: &Vec<Vec<u32>>, index: usize, size: usize, blur_size: usize, round: bool) -> Vec<u32> {
    let length = im.len() as i32;
    let mut ret = vec![0; size];
    let half = (blur_size/2) as i32;
    let index = index as i32;
    let size = size as i32;
    for i in 0..size {
        let mut total = 0_u64;
        let mut count = 0_u64;
        for a in -half..half+1 {
            for b in -half..half+1 {
                if index+a >= 0 && index+a < length && i+b >= 0 && i+b < size {
                    count += 1;
                    total += im[(index+a) as usize][(i+b) as usize] as u64;
                }
            }
        }
        if round {
            ret[i as usize] = (total as f64 / count as f64).round() as u32;
        }else{
            ret[i as usize] = (total / count) as u32;
        }
    }
    ret
}


fn simple_floodfill(im: &mut Vec<Vec<u32>>, growth: i32, road_value: u32) {
    let height = im.len();
    let width = im[0].len();
    let least = 9999;
    let mut n = least+1;
    for y in 0..height {
        for x in 0..width {
            if im[y][x] < least {
                if im[y][x] == road_value{
                    im[y][x] = least;
                }else{
                    _floodfill(im, y, x, n, growth);
                    n += 1;
                }
            }
        }
    }
}

fn _floodfill(im: &mut Vec<Vec<u32>>, y: usize, x: usize, n: u32, growth: i32) {
    let val = im[y][x];
    let height = im.len() as i32;
    let width = im[0].len() as i32;

    let mut q = Vec::new();
    q.push((x, y));
    im[y][x] = n;

    while let Some((x,y)) = q.pop() {
        for i in -growth..growth+1 {
            for j in -growth..growth+1 {
                let x = x as i32;
                let y = y as i32;
                if y+j >= 0 && y+j < height && x+i >= 0 && x+i < width && im[(y+j)as usize][(x+i) as usize] == val {
                    im[(y+j) as usize][(x+i) as usize] = n;
                    q.push(((x+i) as usize, (y+j) as usize));
                }
            }
        }
    }
}

fn save_as_textfile(im: &Vec<Vec<u32>>, output_filename: &str) {
    // collect output into a string
    let output = 
        im.into_par_iter()
        .map(|line| {
            line.iter()
                .map(|x| x.to_string())
                .collect::<Vec<_>>()
                .join(" ")
        })
    .collect::<Vec<_>>()
        .join("\n");

    //create output file
    let output_file = File::create(output_filename.clone())
        .expect(& format!("Unable to create file {}", output_filename));

    //write output to file 
    let mut writer = io::BufWriter::new(&output_file);
    let _ = writer.write_all(output.as_bytes());
}


fn save_as_image(im: &Vec<Vec<u32>>, output_filename: &str, colorstyle: &str) {
    let height = im.len() as i32;
    let width = im[0].len() as i32;

    let mut image = Image::blank( width, height);

    let colors = [
        Color{ r: 255, g: 0, b: 255, a:255 },
        Color{ r: 0, g: 255, b: 255, a:255 },
        Color{ r: 255, g: 0, b: 0, a:255 },
        Color{ r: 0, g: 255, b: 0, a:255 },
        Color{ r: 0, g: 0, b: 255, a:255 },
        Color{ r: 255, g: 0, b: 125, a:255 },
        Color{ r: 255, g: 125, b: 0, a:255 },
        Color{ r: 125, g: 0, b: 255, a:255 },
        Color{ r: 125, g: 255, b: 0, a:255 },
        Color{ r: 255, g: 255, b: 125, a:255 },
        Color{ r: 255, g: 125, b: 255, a:255 },
        Color{ r: 125, g: 255, b: 255, a:255 },
        Color{ r: 255, g: 125, b: 75, a:255 },
        Color{ r: 255, g: 75, b: 125, a:255 },
        Color{ r: 125, g: 255, b: 75, a:255 },
        Color{ r: 125, g: 75, b: 255, a:255 },
        Color{ r: 75, g: 125, b: 255, a:255 },
        Color{ r: 75, g: 255, b: 125, a:255 }
    ];

    let mut n = 0;
    let mut groups = HashMap::new();
    groups.insert(255, Color{ r: 0, g: 0, b: 0, a: 255});
    n += 1;
    for y in 0..height {
        for x in 0..width {
            let yy = y as usize;
            let xx = x as usize;
            if im[yy][xx] == 9999{
                image.set_pixel(x, y, Color {r: 0, g: 0, b: 0, a:255}).unwrap();
            }else{
                let val = im[yy][xx];
                if groups.contains_key(&val) {
                    let color: Color = groups.get(&val).unwrap().clone();
                    image.set_pixel(x, y, color.clone()).unwrap();
                }else{
                    let color = if colorstyle == "Data" {
                        {
                            let val = val as u8;
                            Color{ r: val, g: 255_u8-val, b: 0, a: 255}
                        }
                    }else if colorstyle == "ColorWheel" {
                        colors[n].clone()
                    }else {
                        unimplemented!();
                    };

                    groups.insert(val, color.clone());
                    n += 1;
                    n = n % colors.len();
                    image.set_pixel(x, y, color).unwrap();
                }
            }
        }
    }

    raster::save(&image, &output_filename).unwrap();
}
