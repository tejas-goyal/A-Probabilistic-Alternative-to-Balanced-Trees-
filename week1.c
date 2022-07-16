#include <stdlib.h>

#include <stdio.h>

#include <limits.h>

#include <time.h>

//skip lists

#define SKIPLIST_MAX_LEVEL 6

 

typedef struct snode {

    int key;

    int value;

    struct snode **forward;

} snode;

 

typedef struct skiplist {

    int level;

    int size;

    struct snode *header;

} skiplist;

 

skiplist *skiplist_init(skiplist *list) {

    int i;

    snode *header = (snode *) malloc(sizeof(struct snode));

    list->header = header;

    header->key = INT_MAX;

    header->forward = (snode **) malloc(sizeof(snode*) * (SKIPLIST_MAX_LEVEL + 1));

    for (i = 0; i <= SKIPLIST_MAX_LEVEL; i++) {

        header->forward[i] = list->header;

    }

 

    list->level = 1;

    list->size = 0;

 

    return list;

}

 

static int rand_level() {

    int level = 1;

    while (rand() < RAND_MAX / 2 && level < SKIPLIST_MAX_LEVEL)

        level++;

    return level;

}

 

int skiplist_insert(skiplist *list, int key, int value) {

    snode *update[SKIPLIST_MAX_LEVEL + 1];

    snode *x = list->header;

    int i, level;

    for (i = list->level; i >= 1; i--) {

        while (x->forward[i]->key < key)

            x = x->forward[i];

        update[i] = x;

    }

    x = x->forward[1];

 

    if (key == x->key) {

        x->value = value;

        return 0;

    } else {

        level = rand_level();

        if (level > list->level) {

            for (i = list->level + 1; i <= level; i++) {

                update[i] = list->header;

            }

            list->level = level;

        }

 

        x = (snode *) malloc(sizeof(snode));

        x->key = key;

        x->value = value;

        x->forward = (snode **) malloc(sizeof(snode*) * (level + 1));

        for (i = 1; i <= level; i++) {

            x->forward[i] = update[i]->forward[i];

            update[i]->forward[i] = x;

        }

    }

    return 0;

}

 

snode *skiplist_search(skiplist *list, int key) {

    snode *x = list->header;

    int i;

    for (i = list->level; i >= 1; i--) {

        while (x->forward[i]->key < key)

            x = x->forward[i];

    }

    if (x->forward[1]->key == key) {

        return x->forward[1];

    } else {

        return NULL;

    }

    return NULL;

}

 

static void skiplist_node_free(snode *x) {

    if (x) {

        free(x->forward);

        free(x);

    }

}

 

int skiplist_delete(skiplist *list, int key) {

    int i;

    snode *update[SKIPLIST_MAX_LEVEL + 1];

    snode *x = list->header;

    for (i = list->level; i >= 1; i--) {

        while (x->forward[i]->key < key)

            x = x->forward[i];

        update[i] = x;

    }

 

    x = x->forward[1];

    if (x->key == key) {

        for (i = 1; i <= list->level; i++) {

            if (update[i]->forward[i] != x)

                break;

            update[i]->forward[1] = x->forward[i];

        }

        skiplist_node_free(x);

 

        while (list->level > 1 && list->header->forward[list->level]

                == list->header)

            list->level--;

        return 0;

    }

    return 1;

}

 

static void skiplist_dump(skiplist *list) {

    snode *x = list->header;

    while (x && x->forward[1] != list->header) {

        printf("%d[%d]->", x->forward[1]->key, x->forward[1]->value);

        x = x->forward[1];

    }

    printf("NIL\n");

}

 



//Avl trees

struct Node {
  int key;
  struct Node *left;
  struct Node *right;
  int height;
};

int max(int a, int b);

// Calculate height
int height(struct Node *N) {
  if (N == NULL)
    return 0;
  return N->height;
}

int max(int a, int b) {
  return (a > b) ? a : b;
}

// Create a node
struct Node *newNode(int key) {
  struct Node *node = (struct Node *)malloc(sizeof(struct Node));
  node->key = key;
  node->left = NULL;
  node->right = NULL;
  node->height = 1;
  return (node);
}

// Right rotate
struct Node *rightRotate(struct Node *y) {
  struct Node *x = y->left;
  struct Node *T2 = x->right;

  x->right = y;
  y->left = T2;

  y->height = max(height(y->left), height(y->right)) + 1;
  x->height = max(height(x->left), height(x->right)) + 1;

  return x;
}

// Left rotate
struct Node *leftRotate(struct Node *x) {
  struct Node *y = x->right;
  struct Node *T2 = y->left;

  y->left = x;
  x->right = T2;

  x->height = max(height(x->left), height(x->right)) + 1;
  y->height = max(height(y->left), height(y->right)) + 1;

  return y;
}

int getBalance(struct Node *N) {
  if (N == NULL)
    return 0;
  return height(N->left) - height(N->right);
}

struct Node *insertNode(struct Node *node, int key) {
  if (node == NULL)
    return (newNode(key));

  if (key < node->key)
    node->left = insertNode(node->left, key);
  else if (key > node->key)
    node->right = insertNode(node->right, key);
  else
    return node;

  node->height = 1 + max(height(node->left),
               height(node->right));

  int balance = getBalance(node);
  if (balance > 1 && key < node->left->key)
    return rightRotate(node);

  if (balance < -1 && key > node->right->key)
    return leftRotate(node);

  if (balance > 1 && key > node->left->key) {
    node->left = leftRotate(node->left);
    return rightRotate(node);
  }

  if (balance < -1 && key < node->right->key) {
    node->right = rightRotate(node->right);
    return leftRotate(node);
  }

  return node;
}

struct Node *minValueNode(struct Node *node) {
  struct Node *current = node;

  while (current->left != NULL)
    current = current->left;

  return current;
}

struct Node *deleteNode(struct Node *root, int key) {
  if (root == NULL)
    return root;

  if (key < root->key)
    root->left = deleteNode(root->left, key);

  else if (key > root->key)
    root->right = deleteNode(root->right, key);

  else {
    if ((root->left == NULL) || (root->right == NULL)) {
      struct Node *temp = root->left ? root->left : root->right;

      if (temp == NULL) {
        temp = root;
        root = NULL;
      } else
        *root = *temp;
      free(temp);
    } else {
      struct Node *temp = minValueNode(root->right);

      root->key = temp->key;

      root->right = deleteNode(root->right, temp->key);
    }
  }

  if (root == NULL)
    return root;

  // Update the balance factor of each node and
  // balance the tree
  root->height = 1 + max(height(root->left),
               height(root->right));

  int balance = getBalance(root);
  if (balance > 1 && getBalance(root->left) >= 0)
    return rightRotate(root);

  if (balance > 1 && getBalance(root->left) < 0) {
    root->left = leftRotate(root->left);
    return rightRotate(root);
  }

  if (balance < -1 && getBalance(root->right) <= 0)
    return leftRotate(root);

  if (balance < -1 && getBalance(root->right) > 0) {
    root->right = rightRotate(root->right);
    return leftRotate(root);
  }

  return root;
}

void printPreOrder(struct Node *root) {
  if (root != NULL) {
    printf("%d ", root->key);
    printPreOrder(root->left);
    printPreOrder(root->right);
  }
}

void searchtree(struct Node *root,int ele){
    if(root->key==ele) 
    {
        printf("element %d Found",ele);
        return;
    }
    if(root->key<ele) searchtree(root->right,ele);
    if(root->key>ele) searchtree(root->left,ele);
}






int main() {

    int arr[] = { 3, 6, 9, 2, 11, 1, 4 }, i;

    skiplist list;

    skiplist_init(&list);

    printf("Insert skip list:--------------------\n");

     
    for (i = 0; i < sizeof(arr) / sizeof(arr[0]); i++) {

        skiplist_insert(&list, arr[i], arr[i]);

    }

    
    skiplist_dump(&list);

 

    printf("Search skip list:--------------------\n");
    
   
    
    int keys[] = { 3, 4, 7, 11 };

    double time_spent = 0.0;
 
    clock_t begin = clock();
 
 

    for (i = 0; i < sizeof(keys) / sizeof(keys[0]); i++) {

        snode *x = skiplist_search(&list, keys[i]);

        if (x) {

            printf("key = %d, value = %d\n", keys[i], x->value);

        } else {

            printf("key = %d, not fuound\n", keys[i]);

        }

    }
    
    clock_t end = clock();
    time_spent += (double)(end - begin) / CLOCKS_PER_SEC;
 
    printf("The elapsed search time is %f seconds\n", time_spent);

    printf("\ndelete elements 3,9\n");

    skiplist_delete(&list, 3);

    skiplist_delete(&list, 9);

    skiplist_dump(&list);


    //avl trees

    printf("---avl trees---\n\n");
    printf("Insert avl tree:--------------------\n");
    struct Node *root = NULL;

    for (i = 0; i < sizeof(arr) / sizeof(arr[0]); i++) 
    {
        root = insertNode(root, arr[i]);
    }

    printPreOrder(root);

    printf("\nSearch avl tree:--------------------\n");
    
    time_t start = time(NULL);
 
    for (i = 0; i < sizeof(keys) / sizeof(keys[0]); i++)
    {
        searchtree(root,keys[i]);
        printf("\n");
    }

     time_t finish = time(NULL);
 
    printf("The elapsed search time avl is %d seconds\n",(finish - start));



    printf("\ndelete elements 3,9\n");

    root = deleteNode(root, 3);
    root = deleteNode(root, 9);

    printf("\nAfter deletion: ");
    printPreOrder(root);
 

    return 0;

}