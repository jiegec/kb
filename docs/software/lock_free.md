# Lock Free 数据结构

## Treiber Stack

Treiber Stack 是一个 Lock-Free 的 Stack，支持 Push 和 Pop 操作，出现在 [Systems Programming: Coping With Parallelism](https://dominoweb.draco.res.ibm.com/reports/rj5118.pdf) 第 17 页。原文中，它是由汇编编写的：

<figure markdown>
  ![Treiber Stack](lock_free_treiber_stack_v1.png){ width="400" }
  <figcaption>Treiber Stack（图源 <a href="https://dominoweb.draco.res.ibm.com/reports/rj5118.pdf">Systems Programming: Coping With Parallelism Page 18</a>）</figcaption>
</figure>

翻译成 C++ 代码，它做的事情大概是（参考了 [cppreference](https://en.cppreference.com/w/cpp/atomic/atomic/compare_exchange)）：

```c++
#include <atomic>
#include <optional>

template <class T> struct Node {
  T data;        // user data
  Node<T> *next; // pointer to next node

  Node(const T &data) : data(data), next(nullptr) {}
};

template <class T> struct Stack {
  // paper: ANCHOR
  // head of singly linked list
  std::atomic<Node<T> *> head;

  Stack() : head(nullptr) {}

  // paper: PUTEL
  void push(const T &data) {
    Node<T> *new_head = new Node<T>(data);

    // paper: L R2, ANCHOR
    // read current head
    Node<T> *cur_head = head.load(std::memory_order_relaxed);

    // paper: ST R2, ELNEXT-EL(,R4)
    // link the new list
    new_head->next = cur_head;

    // paper: CS R2, R4, ANCHOR; ST R2, ELNEXT-EL(,R4) on failure
    // atomic swap if head == new_head->next
    // on success: head becomes new_head
    // on failure: new_head->next becomes the current value of head, and loop
    // release order: ensure new_head->next = cur_head is observed before CAS
    while (!head.compare_exchange_weak(new_head->next, new_head,
                                       std::memory_order_release,
                                       std::memory_order_relaxed))
      ;
  }

  // paper: GETEL
  std::optional<T> pop() {
    Node<T> *cur_head;
    // paper: L R2, ANCHOR
    // read current head
    cur_head = head.load(std::memory_order_relaxed);

    // paper: LTR R2, R2; BZ EMPTY
    while (cur_head) {
      // paper: L R4, ELNEXT-EL(,R2)
      // cur_head->next becomes the new list head
      Node<T> *new_head = cur_head->next;

      // paper: CS R2, R4, ANCHOR
      // atomic swap if head == cur_head
      // on success: head becomes new_head
      // on failure: cur_head becomes the current value of head, and loop
      // release order: ensure cur_head->data is done after CAS
      if (head.compare_exchange_weak(cur_head, new_head,
                                     std::memory_order_acquire,
                                     std::memory_order_relaxed)) {
        // success
        T result = cur_head->data;
        delete cur_head;
        return result;
      }
    }

    // no elements
    return {};
  }
};
```

但是这样的实现有一个 ABA 问题：CAS 是根据指针的值来判断是否要 swap，但是指针的值不变，不代表指针指向的还是同一个对象。例如 head 指针（下图的 ANCHOR）指向的 node（下图的 A）被 pop 掉了，未来又重新 push 回来，此时恰好 `new` 出来了同一个指针，就会导致 CAS 写入的 next 指针的值用的是原来的 node（下图的 A）的 next（下图的 B），但这个值是非法的：

<figure markdown>
  ![Treiber Stack ABA Problem](lock_free_treiber_stack_aba.png){ width="400" }
  <figcaption>Treiber Stack 的 ABA 问题（图源 <a href="https://dominoweb.draco.res.ibm.com/reports/rj5118.pdf">Systems Programming: Coping With Parallelism Figure 10 on Page 19</a>）</figcaption>
</figure>

为了解决这个问题，需要把指针和一个整数绑在一起，二者同时 CAS：每次更新指针的时候，就把这个整数加一，这样就可以区分出前后两个 A 指针了，即使它们指针的值相同，但是整数不同，依然可以正常区分。

参考：

- [Systems Programming: Coping With Parallelism](https://dominoweb.draco.res.ibm.com/reports/rj5118.pdf)
- [Treiber stack](https://en.wikipedia.org/wiki/Treiber_stack)
