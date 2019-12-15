#!/usr/bin/env ruby

def fuel n
    return n / 3 - 2
end

sum = 0

File.foreach("input1") {
    |line| sum += fuel(line.to_i)
}

puts sum