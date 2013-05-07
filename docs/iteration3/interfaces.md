Java Interfaces
===============

## GameController Interface
```java

public interface GameControllerInterface {
    public String save();
    public String resume(String key);
    public boolean change_colors(String theme);
    public boolean change_font(String font);
}

```

## Game Interface
```java

public interface GameInterface {
    public String save();
    public String resume(String key);
    public boolean change_colors(String theme);
    public boolean change_font(String font);
}

```

## Player Interface
```java

public interface PlayerInterface {
    public Area current_area();
    public String save();
}

```

## Area Interface
```java

public interface AreaInterface {
    public String description():
}

```

## DataStore Interface
```java

public interface DataStoreInterface {
    public Player get_player();
    pubic boolean put_player(Player p);
}

```
