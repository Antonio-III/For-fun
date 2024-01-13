#include <stdio.h>
#include <stdlib.h>

typedef struct{
    void *next; 
    int data;
}Node;

Node *head=NULL;

// print list
void printList()
{
    Node *current=head;
    int member_count=0;
    printf("The List: ");
    while (current!=NULL)
    {
        if(current->next==NULL)
        {
            printf("%d", current->data);
            member_count+=1;        }
        else
        {
            printf("%d,", current->data);
            member_count+=1;
        }
        current=current->next;
    }
    printf("\nEnd of list\n");
    printf("Member count: %d\n",member_count);
    return;
}
// add node
Node *addNode(int element)
{
    Node *new=NULL;
    // 2 cases
    
    // when 0 elements
    if (head==NULL)
    {
        new= malloc(sizeof(Node));
        if (new==NULL)
        {
            return NULL;
        }
        new->data=element;
        new->next=NULL;
        head=new;
    }
    else // more than 1 element
    {
        new= malloc(sizeof(Node));
        if (new==NULL)
        {
            return NULL;
        }
        new->data=element;
        new->next=head;
        head=new;
    }
    return new;
}
// remove node
int removeNode(int element)
{
    Node *current=head;
    Node *previous=head;
    while(current!=NULL)
    {
        if(current->data==element)
        {
            // deleting the Node the `head` pointer is pointing to.
            if(current==head)
            {
                head=current->next;
            }
            else
            {
                previous->next=current->next;
            }
            free(current);
            current=NULL;
            return 1;
        }
        previous=current;
        current=current->next;
    }   
    return 0;
}
// insert node
Node *insertNode(int element, int index)
{
    Node *new=NULL;
    Node *current=head;
    Node *previous=head;
    int increment=0;
    while(current!=NULL)
    {
        if (increment==index)
        {
            new=malloc(sizeof(Node));
            new->data=element;
            
            if(index==0)
            {
                new->next=head;
                head=new;
            }
            else
            {
                new->next=current;
                previous->next=new;
            }
            return new;
        }
        previous=current;
        current=current->next; 
        increment+=1;
    }
    return NULL;
}
// show options to operate
void showOptions()
{
    printf("You have the options:");
    printf("\n1. Add node\n2. Remove node\n3. Insert node\n4. Print list\n5. Quit\n");
    return;
}
int main(int argc,char**argv) 
{
    // Write C code here
    int option=0;
    int number=0;
    int index=0;
    int members=0;
    while(option!=5)
    {
        showOptions();
        int user_input=scanf("%d", &option);
        if(user_input==1 && option>0 && option<=5)
        {
            switch(option)
            {
                case 1:
                // add 
                    printf("Type a number to add:\n");
                    scanf("%d",&number);
                    Node *add=addNode(number);
                    printf("%d successfully added to the front of the list!\n",number);
                    members+=1;
                    break;
                case 2:
                // remove
                    printf("Type a number to remove:\n");
                    scanf("%d",&number);
                    int success=removeNode(number);
                    if(!success)
                    {
                        printf("%d number not found.\n",number); 
                    }
                    else
                    {
                        printf("Successfully removed 1 left-most instance of %d!\n",number);
                        members-=1;
                    }
                    
                    break;
                break;
                case 3:
                // insert
                    printf("Type a number to insert:\n");
                    scanf("%d",&number);
                    printf("Type an index to insert:\n");
                    scanf("%d",&index);
                    Node *insert=insertNode(number,index);
                    if (insert==NULL)
                    {
                        int available_indices=members-1;
                        if (available_indices==-1)
                        {
                            printf("Index out of range. Member count: %d. Member count must be at least 1. \n",members);
                        }
                        else
                        {
                            printf("Index out of range. Member count: %d. Available indices are from 0 until %d \n",members,available_indices);
                        }
                    }
                    else
                    {
                        printf("%d successfully inserted at index %d!\n",number,index);
                        members+=1;
                    }
                    break;
                case 4:
                    // print list
                    printList();
                    break;
                case 5:
                    // exit
                    printf("Quit program.\n");
                    break; 
            }
        }
    }
    return 0;
}