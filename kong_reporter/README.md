# Kong Log Parser
Specific case log parser.
Sum of hits and bytes sent for clf/elf formatted logs given that:
* Date on record is within 30 days of now
* GET
* The format is exactly as expected (this is where I expect this to fall down)

## Usage
Pipe in logs, returns stdout with a report.
`cat kong_access.log | python parser.py`
