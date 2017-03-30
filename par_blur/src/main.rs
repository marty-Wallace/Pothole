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

    // Set input file for reading
    let inf = File::open(input_filename.clone())
        .expect(& format!("Unable to open file {}", input_filename.clone()));

    let file = BufReader::new(&inf);

    let of = File::create(output_filename.clone())
        .expect(& format!("Unable to create file {}", output_filename));

    let mut writer = io::BufWriter::new(&of);
    
    let im: Vec<Vec<u8>> = 
        file.lines()
        .map(|line| {
            line.unwrap()
                .split_whitespace()
                .map(|x| x.parse().unwrap())
                .collect()
        })
    .collect();

    let size = im[0].len();
    let blur_size = 35;
    let new_im: Vec<Vec<u8>> = 
        (0..im.len())
        .into_par_iter()
        .map(|i| simple_blur(&im, i as usize, size, blur_size))
        .collect();

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

fn simple_blur(im: &Vec<Vec<u8>>, index: usize, size: usize, blur_size: usize) -> Vec<u8> {
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
        ret[i as usize] = (total as f64 / count as f64).round() as u8;
    }
    ret
}

#[cfg(test)]
mod tests {

    #[test]
    fn it_works() {
        let x = 1 + 1;
        assert_eq!(x, 2);
    }
}
