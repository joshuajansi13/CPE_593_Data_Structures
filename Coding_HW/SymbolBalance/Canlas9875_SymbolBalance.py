import re


class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("The stack is empty. Cannot pop.")

    def size(self):
        return len(self.stack)
    
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("The stack is empty. Cannot peek.")
        

class SymbolBalance:
    def __init__(self, inputStr):
        self.infix = inputStr
        self.validOpenSymbols = ['(', '[', '{', '/*']
        self.validCloseSymbols = [')', ']', '}', '*/']
        self.errorMessage = ["NonEmptyStack", "EmptyStack", "Mismatch", "SymbolBalanced"]
        self.operators = ['+', '-', '*', '/']

    def parseInput(self):
        self.infix = self.infix.replace(" ", "") # remove white spaces 
        status, output = self.checkSyntax()
        if status == self.errorMessage[3]:
            parsedInput = re.sub(r'/\*.*\*/', '', self.infix) # remove any comments
        else:
            parsedInput = self.infix
        return parsedInput, status, output

    def checkSyntax(self):
        symbolStack = Stack()
        for item in self.infix:
            if item in self.validOpenSymbols:
                symbolStack.push(item)
            elif item in self.validCloseSymbols:
                if symbolStack.is_empty(): # EmptyStack error
                    return self.errorMessage[1], item 
                else:
                    # get index for open and close symbols for comparison
                    openIndex = self.validOpenSymbols.index(symbolStack.peek()) # check the top of the stack
                    closeIndex = self.validCloseSymbols.index(item)
                    if openIndex != closeIndex: # Mismatch error
                        return self.errorMessage[2], self.validOpenSymbols[openIndex] + self.validCloseSymbols[closeIndex]
                    else:
                        symbolStack.pop()

        if not symbolStack.is_empty(): # NonEmptyStack error
            return self.errorMessage[0], symbolStack.peek()
        
        return self.errorMessage[3], "" # SymbolBalanced


    def postfixExpress(self, parsedString):
        outputString = ""
        symbolStack = Stack()
        for item in parsedString:
            if item.isalnum(): # operand
                outputString += item
            elif item in self.validOpenSymbols:
                symbolStack.push(item)
            elif item in self.validCloseSymbols:
                index = self.validCloseSymbols.index(item)
                while symbolStack.peek() != self.validOpenSymbols[index]:
                    outputString += symbolStack.pop()
                symbolStack.pop()
            elif item in self.operators:
                if symbolStack.is_empty():
                    symbolStack.push(item)
                else:                        
                    if item == self.operators[2] or item == self.operators[3]:
                        if (symbolStack.peek() == self.operators[2]) or (symbolStack.peek() == self.operators[3]):
                            outputString += symbolStack.pop()
                        symbolStack.push(item)
                    elif item == self.operators[0] or item == self.operators[1]:
                        while symbolStack.peek() in self.operators:
                            if (symbolStack.peek() == self.operators[0]) or (symbolStack.peek() == self.operators[1]):
                                outputString += symbolStack.pop()
                                break
                            elif (symbolStack.peek() == self.operators[2]) or (symbolStack.peek() == self.operators[3]):
                                outputString += symbolStack.pop()
                                if symbolStack.is_empty() or symbolStack.peek() not in self.operators:
                                    break
                        symbolStack.push(item)
                        
        while not symbolStack.is_empty():
            outputString += symbolStack.pop()

        return outputString


def runSymbolBalance(inputStr):
    # This will test all of the different errors and run postfixExpress, if symbols are balanced
    print(f"The input string is: \"{inputStr}\"")
    symbolBalanceTest = SymbolBalance(inputStr)
    parsedInput, statusMessage, outputSymbols = symbolBalanceTest.parseInput()

    if statusMessage == "SymbolBalanced":
        # run postfixExpress and print out postfix expression
        postfixExpr = symbolBalanceTest.postfixExpress(parsedInput)
        print("This input is symbolically balanced.")
        print(f"The postfix expression for this input is: {postfixExpr} \n")
    else:
        print(f"This is a {statusMessage} Error.")
        print(f"Output Symbols: {outputSymbols} \n")



# Define different input strings and call runSymbolBalance to get different outputs
NonEmptyStackCheck = "a + [ b * c + { d * e + f } * g  /* this input is testing for NonEmptyStack error */"  # The input ends with one or more symbols missing their corresponding closing symbols
EmptyStackCheck = "a + [ b * c + d * e + f ] ) * g  /* this input is testing for EmptyStack error */"  # There is a closing symbol without its corresponding opening symbol
MismatchCheck = "a + [ b * c + ( d * e + f ] ) * g  /* this input is testing for Mismatch error */"  # There is a mismatch between closing and opening symbols, e.g. { ( } )
SymbolBalancedCheck_1 = "a + [ b * c + ( d * e + f ) ] * g  /* this input is testing for SymbolBalanced */"  # No error is found
SymbolBalancedCheck_2 = "a + b * c + ( d * e + f ) * g  /* this input is testing for SymbolBalanced */"  # No error is found


# Run some tests for proof
runSymbolBalance(NonEmptyStackCheck)
runSymbolBalance(EmptyStackCheck)
runSymbolBalance(MismatchCheck)
runSymbolBalance(SymbolBalancedCheck_1)
runSymbolBalance(SymbolBalancedCheck_2)
