extern crate rayon; 

use std::io;
use std::io::prelude::*;
use std::io::BufReader;
use std::io::BufRead;
use std::fs::File;
use std::env;
use rayon::prelude::*;

fn main() {
    let input_filename = env::args().nth(1).expect("Supply input_filename as arg[1]");
    let output_filename= env::args().nth(2).expect("Supply output_filename as arg[2]");
    let size = match env::args().nth(3) {
        Some(x) => x.parse::<usize>().expect("Supply integer argument for blur size as arg[3]"),
        _ => 35,
    };

    // Set input file for reading
    let inf = File::open(input_filename.clone())
        .expect(& format!("Unable to open file {}", input_filename.clone()));

    let file = BufReader::new(&inf);

    let of = File::create(output_filename.clone())
        .expect(& format!("Unable to create file {}", output_filename));

    let mut writer = io::BufWriter::new(&of);
    
    let mut im: Vec<Vec<u32>> = 
        file.lines()
        .map(|line| {
            line.unwrap()
                .split_whitespace()
                .map(|x| x.parse().unwrap())
                .collect()
        })
    .collect();

    let blur = false;

    let new_im;
    if blur {
        new_im = do_blur(&im, size)
    }else{
        simple_floodfill(&mut im, size as i32);
        new_im = im;
    }
    
    let output = 
        new_im.into_par_iter()
        .map(|line| {
            line.iter()
                .map(|x| x.to_string())
                .collect::<Vec<_>>()
                .join(" ")
        })
        .collect::<Vec<_>>()
        .join("\n");

    let _ = writer.write_all(output.as_bytes());
}

fn do_blur(im: &Vec<Vec<u32>>, blur_size: usize) -> Vec<Vec<u32>> {

    let size = im[0].len();
    // collect blurred image from parallel iterators

    (0..im.len())
    .into_par_iter()
    .map(|i| simple_blur(&im, i as usize, size, blur_size))
    .collect()
}

fn simple_blur(im: &Vec<Vec<u32>>, index: usize, size: usize, blur_size: usize) -> Vec<u32> {
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
        ret[i as usize] = (total as f64 / count as f64).round() as u32;
    }
    ret
}


fn simple_floodfill(im: &mut Vec<Vec<u32>>, growth: i32) {
    let height = im.len();
    let width = im[0].len();
    let least = 9999;
    let mut n = least+1;
    for y in 0..height {
        for x in 0..width {
            if im[y][x] < least {
                if im[y][x] == 127 {
                    im[y][x] = 9999;
                }else{
                    _floodfill(im, y, x, n, growth);
                    n += 1;
                }
            }
        }
    }
}

fn _floodfill(im: &mut Vec<Vec<u32>>, y: usize, x: usize, n: u32, growth: i32) {
    let value = im[y][x];
    let height = im.len() as i32;
    let width = im[0].len() as i32;

    let mut q = Vec::new();
    q.push((x, y));

    while let Some((x,y)) = q.pop() {
        im[y][x] = n;
        for i in -growth..growth+1 {
            for j in -growth..growth+1 {
                let x = x as i32;
                let y = y as i32;
                if y+j >= 0 && y+j < height && x+i >= 0 && x+i < width && im[(y+j)as usize][(x+i) as usize] != 9999 && im[(y+j) as usize][(x+i) as usize] != 127 {
                    q.push(((x+i) as usize, (y+j) as usize));
                }
            }
        }
    }
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        let x = 1 + 1;
        assert_eq!(x, 2);
    }
}
