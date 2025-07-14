# RCU (Read-Copy-Update)

RCU 是一种读写锁的替代方案，主要针对以读为主的 workload，它的思路是：

- writer 要更新被保护的对象的时候，不修改已有的对象，而是生成一个新的 copy，然后原子地进行对象引用的替换；那么 reader 此时依然可以正常访问对象，只不过可能访问的是修改前的版本，也可能访问的是修改后的版本
- writer 如果要删除某个对象，首先把对这个对象的引用修改掉，使得未来的 reader 不会再访问该对象；然后等待所有正在进行的 reader 完成它们的处理，此时这个对象一定没有 reader 在访问，于是可以进行回收
- 如果有多个 writer，那么 writer 之间依然需要用互斥锁保护，保证只有一个 writer 同时在修改

## Linux 内核中的 RCU

reader 一侧要做的事情：

1. 调用 `rcu_read_lock()`，表示 reader 读取对象的区间的开始
2. 使用 `rcu_dereference(pointer)` 来对指针进行解引用
3. 调用 `rcu_read_unlock()`，表示 reader 读取对象的区间的结束

writer 一侧要做的事情：

1. 如果是多个 writer，首先获取互斥锁：`spin_lock(mutex)`
2. 调用 `rcu_dereference_protected()` 来对指针进行解引用，得到原值
3. 调用 `kmalloc()` 以创建新的对象，再基于上一步读取的原值进行修改
4. 调用 `rcu_assign_pointer()` 把指针指向新的对象
5. 如果是多个 writer，释放互斥锁：`spin_lock(mutex)`
6. 调用 `synchronize_rcu()` 等待所有正在进行的 reader 完成读取（即调用 `rcu_read_unlock`）
7. 调用 `kfree` 把原来的旧对象释放掉

参考：

- [What is RCU? -- “Read, Copy, Update”](https://www.kernel.org/doc/html/next/RCU/whatisRCU.html)
