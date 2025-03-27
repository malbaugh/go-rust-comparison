// main.go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

type User struct {
    ID   string `json:"id"`
    Name string `json:"name"`
}

var users = make(map[string]User)

func main() {
    r := gin.Default()

    r.POST("/users", func(c *gin.Context) {
        var user User
        if err := c.BindJSON(&user); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        users[user.ID] = user
        c.JSON(http.StatusCreated, user)
    })

    r.GET("/users/:id", func(c *gin.Context) {
        id := c.Param("id")
        user, ok := users[id]
        if !ok {
            c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
            return
        }
        c.JSON(http.StatusOK, user)
    })

    r.PUT("/users/:id", func(c *gin.Context) {
        id := c.Param("id")
        var user User
        if err := c.BindJSON(&user); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        user.ID = id
        users[id] = user
        c.JSON(http.StatusOK, user)
    })

    r.DELETE("/users/:id", func(c *gin.Context) {
        id := c.Param("id")
        delete(users, id)
        c.Status(http.StatusNoContent)
    })

    r.Run(":8080")
}
