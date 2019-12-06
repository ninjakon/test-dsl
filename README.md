# Test DSL
##### Language-independent Software Testing
##### Advanced Software Engineering WS19/20

## Outline
- Allows specification of langauge-independent tests using a pre-defined dsl
- Offers several run options: all-tests / single-test / verbose
- Currently supports Python and Javascript

## Usage
\> python3 test-dsl -t <test_suite_file> [Optional]

###### Required
| short   | long          | arg               | description             |
| :------ | :-----------  | :---------------- | :---------------------- |
| -t      | --test-suite= | <test_suite_file> | specify test suite file |

###### Optional
| short   | long           | arg               | description                      |
| :------ | :-----------   | :---------------- | :----------------------          |
| -h      | --help         |                   | show usage                       |
| -v      | --verbose      |                   | set test suite output verbose    |
| -a      | --all-tests    |                   | run all tests in test suite      |
| -s      | --single-tests | <test1/test2/...> | run list of single tests         |
| -l      | --language     | <py&#124;js>      | specify language (py is default) |

## How it works
1. Load meta model using textX.
2. Load test suite model with meta model.
3. Instantiate TestSuite class corresponding to language.
4. Let TestSuite interpret the model by registering test suite components: Actors, BeforeAlls, Befores, Tests, Afters and AfterAll.
5. Run an arbitrary number of tests: For Python tests can be run natively. For Javascript components have to be passed to a Javascript Helper.
