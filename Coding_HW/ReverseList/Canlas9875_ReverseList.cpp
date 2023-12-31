#include <iostream>
#include <string>
#include <cctype>


class Node
{

private:
    char value;
    Node* next;

public:
    Node(char data) 
    {
        value = data;
        next = nullptr;
    }
    char getValue()
    {
        return value;
    }
    void setValue(char data)
    {
        value = data;
    }
    Node* getNext()
    {
        return next;
    }
    void setNext(Node* nextPtr)
    {
        next = nextPtr;
    }
};

class LinkedList 
{

private:
    Node* head;

public:
    LinkedList()
    {
        head = nullptr;
    }
    
    void insertNode(char data)
    {
        Node* newNode = new Node(data);
        if (head)
        {
            Node* currentNode = head;
            while (currentNode->getNext())
            {
                currentNode = currentNode->getNext();
            }
            currentNode->setNext(newNode);
        }
        else
        {
            head = newNode;
        }
    }

    void reverseLinkedList()
    {
        Node* prevNode = nullptr;
        Node* currentNode = head;
        Node* nextNode = nullptr;

        while (currentNode)
        {
            nextNode = currentNode->getNext();
            currentNode->setNext(prevNode);
            prevNode = currentNode;
            currentNode = nextNode;
        }

        head = prevNode;
    }

    Node* getHead()
    {
        return head;
    }

    void cleanLinkedList()
    {
        Node* currentNode = head;
        while(currentNode->getNext())
        {
            Node* nextNode = currentNode->getNext();
            delete currentNode;
            currentNode = nextNode;
        }
        head = nullptr;
    }

    void printLinkedList()
    {
        Node* currentNode = head;
        while (currentNode)
        {
            std::cout << currentNode->getValue();
            currentNode = currentNode->getNext();
        }
    }

    void printIsPalindrome(std::string input)
    {
        Node* currentNode = head;
        for (int i = 0; i < input.length(); i++)
        {
            while(!std::isalpha(currentNode->getValue()))
            {
                currentNode = currentNode->getNext(); // Skip over the nodes that contain non-letter values
            }

            if (!std::isalpha(input[i]))
            {
                continue; // Ignore whitespaces and non-letter values in input string
            }

            if (std::tolower(currentNode->getValue()) != std::tolower(input[i]))
            {
                std::cout << "\"" << input << "\"" << " is not a palindrome." << std::endl;
                return;
            }
            currentNode = currentNode->getNext();
        }
        std::cout << "\"" << input << "\"" << " is a palindrome." << std::endl;
    }
};


int main()
{
    // Take user input
    std::string userInput;
    std::cout << "Enter a string: ";
    std::getline(std::cin, userInput);

    // Put the input string into a linked list
    LinkedList inputString;
    for (int i = 0; i < userInput.length(); i++)
    {
        inputString.insertNode(userInput[i]);
    }

    // Print out the input string
    std::cout << "Input string: ";
    inputString.printLinkedList();
    std::cout<< std::endl;

    // Reverse the string and print out the result
    inputString.reverseLinkedList();
    std::cout << "Reversed string: ";
    inputString.printLinkedList();
    std::cout<< std::endl;

    // Print out if string is a palindrome here
    inputString.printIsPalindrome(userInput);

    // Clean up linked list
    inputString.cleanLinkedList();

    return 0;
}
