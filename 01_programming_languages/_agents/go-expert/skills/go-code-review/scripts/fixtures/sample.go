package sample

import (
	"os"
	"math/rand"
	"sync"
	"time"
)

type Account struct{ owner string }

func (a *Account) GetOwner() string { return a.owner }

func (a *Account) Owner() string { return a.owner }

func seed() { rand.Seed(time.Now().UnixNano()) }

func bad(mu *sync.Mutex) {
	mu.Lock()
	time.Sleep(time.Second)
	mu.Unlock()
}

func good(mu *sync.Mutex) {
	mu.Lock()
	defer mu.Unlock()
}

func loops(items []string) {
	for _, it := range items {
		go func() {
			println(it)
		}()
	}
	for i := 0; i < 3; i++ {
		defer println(i)
	}
}

func recovers() {
	defer func() {
		if r := recover(); r == nil {
			return
		}
	}()
	panic(nil)
}

func openIt(path string, ch chan int) {
	f, _ := os.Open(path)
	_ = f
	for {
		select {
		case v := <-ch:
			println(v)
		default:
		}
	}
}
