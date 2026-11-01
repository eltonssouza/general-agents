// Test fixture (own example, not from the book): code with no detectable smells.
public class Limpo {
    private static final int SECONDS_PER_DAY = 86400;

    public boolean expired(Session session) {
        return session.ageInSeconds() > SECONDS_PER_DAY;
    }
}
