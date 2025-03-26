from antlr4 import *
from ArithmeticLexer import ArithmeticLexer
from ArithmeticParser import ArithmeticParser
import sys

class ArithmeticVisitor:
    def __init__(self) -> None:
        # Dicionário para armazenar variáveis e seus valores
        self.memory = {}
        
    def visit(self, ctx):
        # Método genérico para visitar diferentes tipos de nós na árvore de análise.
        if isinstance(ctx, ArithmeticParser.ProgramContext):
            return self.visitProgram(ctx)
        elif isinstance(ctx, ArithmeticParser.StatementContext):
            return self.visitStatement(ctx)
        elif isinstance(ctx, ArithmeticParser.AssignmentContext):
            return self.visitAssignment(ctx)
        elif isinstance(ctx, ArithmeticParser.ExprContext):
            return self.visitExpr(ctx)
        elif isinstance(ctx, ArithmeticParser.TermContext):
            return self.visitTerm(ctx)
        elif isinstance(ctx, ArithmeticParser.FactorContext):
            return self.visitFactor(ctx)
        
    def visitProgram(self, ctx):
        # Visita o nó do programa, que contém múltiplas declarações.
        results = []
        for statement in ctx.statement():
            results.append(self.visit(statement))
        return results
    
    def visitStatement(self, ctx):
        # Visita uma declaração, que pode ser uma atribuição ou uma expressão.
        return self.visit(ctx.getChild(0))
    
    def visitAssignment(self, ctx):
        # Visita uma atribuição e armazena o valor da variável na memória.
        var_name = ctx.VAR().getText()
        value = self.visit(ctx.expr())
        self.memory[var_name] = value
        return value

    def visitExpr(self, ctx):
        # Visita uma expressão, que pode conter termos separados por '+' ou '-'.
        result = self.visit(ctx.term(0))
        for i in range(1, len(ctx.term())):
            op = ctx.getChild(i * 2 - 1).getText()
            if op == '+':
                result += self.visit(ctx.term(i))
            elif op == '-':
                result -= self.visit(ctx.term(i))
            else:
                raise Exception(f"Operador inválido: {op}")
        return result

    def visitTerm(self, ctx):
        # Visita um termo, que pode conter fatores separados por '*' ou '/'.
        result = self.visit(ctx.factor(0))
        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(i * 2 - 1).getText()
            if op == '*':
                result *= self.visit(ctx.factor(i))
            elif op == '/':
                next_factor = self.visit(ctx.factor(i))
                if next_factor != 0:
                    result /= next_factor
                else:
                    raise Exception("Erro: Divisão por zero")
        return result

    def visitFactor(self, ctx):
        # Visita um fator, que pode ser um número inteiro, uma variável ou uma expressão entre parênteses.
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.VAR():
            var_name = ctx.VAR().getText()
            if var_name in self.memory:
                return self.memory[var_name]
            else:
                raise Exception(f"Erro: Variável indefinida '{var_name}'")
        else:
            return self.visit(ctx.expr())


def process_expression(expression, visitor):
    # Processa uma única expressão usando o lexer, parser e visitor.
    lexer = ArithmeticLexer(InputStream(expression))
    stream = CommonTokenStream(lexer)
    parser = ArithmeticParser(stream)
    tree = parser.program()
    return visitor.visit(tree)


def main():
    visitor = ArithmeticVisitor()

    if len(sys.argv) > 1:
        # Modo de execução por arquivo
        file_path = sys.argv[1]
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                expressions = f.readlines()
            
            for expression in expressions:
                expression = expression.strip()
                if expression:
                    try:
                        result = process_expression(expression, visitor)
                        if result is not None:
                            print(f'Resultado da expressão "{expression}":', result)
                    except Exception as e:
                        print(f"Erro ao processar a expressão '{expression}': {e}")

        except FileNotFoundError:
            print(f"Erro: Arquivo '{file_path}' não encontrado.")
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
    else:
        # Modo interativo (REPL)
        print("REPL de Aritmética. Digite 'exit' para sair.")
        while True:
            try:
                expression = input(">>> ")
                if expression.strip().lower() == 'exit':
                    print("Saindo...")
                    break

                result = process_expression(expression, visitor)
                if result is not None:
                    print(f'Resultado da expressão "{expression}":', result)
            except Exception as e:
                print(f"Erro: {e}")


if __name__ == '__main__':
    main()
