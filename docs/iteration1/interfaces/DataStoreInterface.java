import java.util.List;

public interface DataStoreInterface {
    public Area getArea(String id);
    public Player getPlayer(String id);
    public Item getItem(String name);
    public List<Character> getCharacters(String name);
}
