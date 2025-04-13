class BasicVisitor:
    def __init__(self):
        self.variables = {}

    def visit_program(self, program):
        for statement in program['statements']:
            self.visit(statement)

    def visit_print(self, statement):
        print(statement['value'])

    def visit_decl(self, statement):
        var_name = statement['name']
        self.variables[var_name] = None

    def visit_input(self, statement):
        var_name = statement['name']
        user_input = input()
        self.variables[var_name] = int(user_input)

    def visit_if(self, statement):
        condition = self.evaluate_expression(statement['condition'])
        if condition:
            for stmt in statement['statements']:
                self.visit(stmt)

    def evaluate_expression(self, expression):
        if isinstance(expression, int):
            return expression
        elif isinstance(expression, str):
            return self.variables.get(expression, 0)
        elif isinstance(expression, dict):
            left = self.evaluate_expression(expression['left'])
            right = self.evaluate_expression(expression['right'])
            op = expression['op']
            if op == '>':
                return left > right
            elif op == '<':
                return left < right
            elif op == '==':
                return left == right
        return False

    def visit(self, statement):
        statement_type = statement['type']
        if statement_type == 'PRINT':
            self.visit_print(statement)
        elif statement_type == 'DECL':
            self.visit_decl(statement)
        elif statement_type == 'INPUT':
            self.visit_input(statement)
        elif statement_type == 'IF':
            self.visit_if(statement)


# Example of how the program could be represented as a dictionary
program = {
    'statements': [
        {'type': 'PRINT', 'value': 'Type a number'},
        {'type': 'DECL', 'name': 'num'},
        {'type': 'INPUT', 'name': 'num'},
        {'type': 'IF', 'condition': {'left': 'num', 'op': '>', 'right': 100}, 'statements': [
            {'type': 'PRINT', 'value': 'Maior que 100'}
        ]},
        {'type': 'IF', 'condition': {'left': 'num', 'op': '<', 'right': 100}, 'statements': [
            {'type': 'PRINT', 'value': 'Menor que 100'}
        ]},
        {'type': 'IF', 'condition': {'left': 'num', 'op': '==', 'right': 100}, 'statements': [
            {'type': 'PRINT', 'value': 'Digitou 100'}
        ]}
    ]
}

# Running the visitor
visitor = BasicVisitor()
visitor.visit_program(program)