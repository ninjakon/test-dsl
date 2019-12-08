const argType = {
    actor_definitions: 2,
    before_all: 3,
    befores: 4,
    tests: 5,
    afters: 6,
    after_all: 7,
    verbose: 8
};

const testBlock = {
    before: 0,
    execute: 1,
    after: 2
};

const tText = {
    INFO: '\033[94m',
    OK: '\033[92m',
    WARN: '\033[93m',
    FAIL: '\033[91m',
    BOLD: '\033[1m',
    UL: '\033[4m',
    ENDC: '\033[0m'
};

/* *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  Log */
function print_if_verbose(msg, tb_lvl = 0) {
    if (verbose) {
        let output = '';
        for (let i = 0; i < tb_lvl; i++) {
            output += '\t';
        }
        output += msg;
        console.log(output + tText.ENDC);
    }
}

/* *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *Test Report */
const test_report = {
    BA: [],
    TC: 0,
    CT: [null, []],
    ST: [],
    FT: [],
    AA: []
};

let add_error_fun = null;

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  Testing Arguments */
const actor_definitions = JSON.parse(process.argv[argType.actor_definitions]);
const before_all = JSON.parse(process.argv[argType.before_all]);
const befores = JSON.parse(process.argv[argType.befores]);
const tests = JSON.parse(process.argv[argType.tests]);
const afters = JSON.parse(process.argv[argType.afters]);
const after_all = JSON.parse(process.argv[argType.after_all]);
const verbose = process.argv[argType.verbose] === 'True';

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *Testing */
function process_ba_aa(type, steps, callback) {
    print_if_verbose(tText.INFO + (type.localeCompare('BA') === 0 ? 'Running BeforeAll' : 'Running AfterAll'));
    add_error_fun = (l, e) => {
        test_report[type].push([l + tText.ENDC, e + tText.ENDC])
    };
    process_steps(steps, true, 1, callback);
}

function process_before_after_test(type, blocks, references, callback) {
    if (references.length > 0) {
        print_if_verbose(tText.INFO + 'Running ' + type, 1);
    }
    add_error_fun = (l, e) => {
        test_report.CT[1].push([tText.INFO + 'In ' + type + ' Clause: ' + l + tText.ENDC, e + tText.ENDC])
    };
    const recursive_b_a = (i) => {
        if (i < references.length) {
            process_steps(blocks[references[i]], true, 2, () => recursive_b_a(i + 1));
        } else {
            callback();
        }
    };
    recursive_b_a(0);
}

function process_tests(test_names, callback) {
    const recursive_test = (i) => {
        if (i < test_names.length) {
            let test_name = test_names[i];
            console.log(tText.INFO + 'Running ' + test_name + tText.ENDC);
            test_report.CT = [test_name, []];
            process_test(test_name, () => recursive_test(i + 1));
        } else {
            callback();
        }
    };
    recursive_test(0);
}

function process_test(test_name, callback) {
    const test = tests[test_name];
    /* execute before test -> callback: tests */
    process_before_after_test('Before', befores, test[testBlock.before], () => {
        /* execute test -> callback: after test */
        process_steps(test[testBlock.execute], false, 2, () => {
            /* execute after test -> callback: next test */
            process_before_after_test('After', afters, test[testBlock.after], () => {
                const errors = test_report.CT[1];
                if (errors.length === 0) {
                    test_report.ST.push(test_report.CT[0]);
                } else {
                    test_report.FT.push(test_report.CT);
                }
                test_report.TC += 1;
                test_report.CT = [null, []];

                callback();
            });
        });
    });
}

/* *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  Step Processing */
function process_steps(steps, is_ba, tb_lvl, callback) {
    if (!is_ba) {
        print_if_verbose(tText.INFO + 'Executing Test', 1);
        add_error_fun = (l, e) => test_report.CT[1].push([l + tText.ENDC, e + tText.ENDC]);
    }
    const recursive_step = (i) => {
        if (i < steps.length) {
            if (is_ba) {
                print_if_verbose(tText.INFO + '"' + steps[i][0] + '" OK', 2);
            }
            process_step(steps[i], tb_lvl, () => recursive_step(i + 1));
        } else {
            callback();
        }
    };
    recursive_step(0);
}

function process_step(step, tb_lvl, callback) {
    const type = step[0][0];
    const args = step[0][1];
    switch (type) {
        case 'AssertStep':
            process_assert_step(args, step[1], tb_lvl, callback);
            break;
        case 'AssignStep':
            process_assign_step(args, callback);
            break;
        case 'CallStep':
            process_call_step(args, callback);
            break;
        case 'TimeStep':
            process_time_step(args, callback);
            break;
    }
}

/* *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * Specified Step Processing */
function process_assert_step(args, position, tb_lvl=2, callback) {
    const actor_name = args[0];
    const actor = actors[actor_name];
    const attribute = args[1];
    const expected_value = args[2];
    const actual_value = actor[attribute];

    const is_ok = actual_value === expected_value;
    let message = '';
    if (!is_ok) {
        const line_info = tText.WARN + 'Assertion ' + tText.BOLD + 'ERROR' + tText.ENDC +
            tText.WARN + ' in ' + tText.UL + 'line ' + position[0] + ' column ' + position[1] + ':' + tText.ENDC;
        const error = style_assertion(is_ok, actor_name, attribute, expected_value, actual_value);
        add_error_fun(line_info, error + tText.ENDC);
        message = line_info + '\n';
        for (var i = 0; i < tb_lvl; i++) {
            message += '\t';
        }
        message += error;
    } else {
        message = style_assertion(is_ok, actor_name, attribute, expected_value, actual_value);
    }
    print_if_verbose(message, 2);
    callback();
}

function process_assign_step(args, callback) {
    const actor = actors[args[0]];
    const attribute = args[1];
    actor[attribute] = args[2];
    callback();
}

function process_call_step(args, callback) {
    const actor = actors[args[0]];
    const method = args[1];
    const params = [];
    for (let j = 0; j < args[2].length; j++) {
        const is_actor = args[2][j][0];
        const param = args[2][j][1];
        is_actor ? params.push(actors[param]) : params.push(param);
    }
    actor[method](...params);
    callback();
}

function process_time_step(args, callback) {
    setTimeout(callback, args[0]);
}

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *Assertions */
function style_assertion(is_ok, actor_name, attribute, expected_value, actual_value) {
    let infix, suffix, color;
    if (is_ok) {
        infix = 'and was';
        suffix = '.';
        color = tText.OK;

    } else {
        infix = 'but was';
        suffix = '!';
        color = tText.FAIL;
    }
    return color + 'Expected' + tText.BOLD + ` ${actor_name}[${attribute}]` + tText.ENDC +
        color + ' == ' + tText.BOLD + `${expected_value} ` + tText.ENDC +
        color + infix + tText.BOLD + ` ${actual_value}` + tText.ENDC +
        color + suffix
}

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * Actors */
const actors = {};
function ActorTblRow(instance, class_name, attributes) {
    this.instance = instance;
    this.class_name = class_name;
    this.attributes = attributes;
}
const actor_tbl = [];
for (let actor_name in actor_definitions) {
    /* check for IDE */
    if (!actor_definitions.hasOwnProperty(actor_name)) {
        break;
    }

    /* instantiate classes */
    const module = actor_definitions[actor_name][0];
    const actor_class = require(module);
    actors[actor_name] = new actor_class();

    /* set pre-defined attributes */
    const attributes = actor_definitions[actor_name][1];
    for (let i = 0; i < attributes.length; i++) {
        const attribute_name = attributes[i][0];
        // check if attribute exists in class
        if (!actors[actor_name].hasOwnProperty(attribute_name)) {
            throw new Error('Non-existing attribute: ' + actor_name + '[' + attribute_name + ']!')
        }
        actors[actor_name][attribute_name] = attributes[i][1];
    }

    /* append to actor table */
    actor_tbl.push(new ActorTblRow(actor_name, module, JSON.stringify(actors[actor_name])));
}
if (verbose) {
    console.table(actor_tbl);
}

/*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * Callback Hell*/
process_ba_aa('BA', before_all, () => {
    process_tests(Object.keys(tests), () => {
        process_ba_aa('AA', after_all, () => {
            console.log(JSON.stringify({test_report: test_report}));
        });
    });
});
