def stringify(string):
    if not isinstance(string, str): return string
    return '"' + str(string) + '"'


def stringify_steps(steps):
    return [stringify_step(s) for s in steps]


def stringify_step(step):
    step_type = step.__class__.__name__
    step_vars = []
    if step_type == 'AssignStep':
        step_vars.append(stringify(step.attributeReference.actor.name))
        step_vars.append(stringify(step.attributeReference.attribute.name))
        step_vars.append(stringify(step.value))
    elif step_type == 'CallStep':
        step_vars.append(stringify(step.actor.name))
        step_vars.append(stringify(step.method))
        parameters = [(False, p.value) if p.actor is None else (True, stringify(p.actor.name)) for p in step.parameters]
        step_vars.append(parameters)
    elif step_type == 'AssertStep':
        step_vars.append(stringify(step.attributeReference.actor.name))
        step_vars.append(stringify(step.attributeReference.attribute.name))
        step_vars.append(stringify(step.value))
    elif step_type == 'TimeStep':
        step_vars.append(step.delay)
    return [stringify(step_type), step_vars]
