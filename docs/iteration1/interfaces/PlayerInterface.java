import java.util.List;

public interface PlayerInterface {
    public List<Item> getAllItems();
    public Player getPlayer(String id);
    public Area getDirection(String direction);
    public Area getCurrentArea();
    public Boolean setArea(Area a);
    public Item getItem(String name);
    public String eatItem(String name);
}
