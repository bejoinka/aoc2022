const { Command } = require("commander");
const fs = require("fs")

const program = new Command();

program
    .name("aoc2022")
    .description("advent of code in typescript")
    .version("1.0.0");

program
    .command("aoc")
    .description("run for a given day")
    .argument("day", "which day to grab")
    .option("-p, --part <part>", 'which part', '1')
    .action((day, options) => {
        const dayAsNumber = new Number(day)
        if (dayAsNumber == NaN || dayAsNumber < 1 || dayAsNumber > 25) {
            throw new Error("the day must be a number between 1 and 25")
        }
        if (dayAsNumber < 10) {
            day = `0${dayAsNumber}`
        } else {
            day = `${dayAsNumber}`
        }
        try {
            file = require(`./day${day}/day${dayAsNumber}.js`)
            options.input = fs.readFileSync(`./day${day}/input.txt`).toString().trim()
            file.run(options)
        } catch (err) {
            console.error(err)
        }
    })

program.parse();