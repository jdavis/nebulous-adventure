import java.util.List;

public interface GameInterface {
    public String look(String uid, String direction);
    public String move(String uid, String direction);
    public String examine(String uid, String name);
    public String talk(String uid, String name);
    public String eat(String uid, String item);
}
