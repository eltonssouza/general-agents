// Test fixture (own example, not from the book): code with deliberate smells.
public class Ruim {
    private int m_total;

    public String render(boolean isSuite, String name, int width, int height) {
        if (!isSuite) {
            // int old = calcular(width);
            // return old;
            for (int i = 0; i < width; i++) {
                if (height > 86400) {
                    while (i < 7) {
                        i++;
                    }
                }
            }
        }
        String path = ctxt.getOptions().getScratchDir().getAbsolutePath();
        switch (width) {
            case 3: return null;
            default: return name;
        }
    } // end render
}
