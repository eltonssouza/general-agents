import java.io.*;
import java.util.*;

public class Sample {
    public static boolean same(String a) {
        if (a == "abc") {            // reference comparison
            return true;
        }
        return a.equals("abc");      // correct
    }

    protected void finalize() {       // finalizer
    }

    public List<String> names(boolean any) {
        if (!any) {
            return null;             // null collection
        }
        return new ArrayList<>();
    }

    public String firstLine(String path) throws IOException {
        BufferedReader r = new BufferedReader(new FileReader(path));   // no try-with-resources
        try {
            return r.readLine();
        } catch (IOException e) {
        }
        return null;
    }

    public String ok(String path) throws IOException {
        try (BufferedReader r = new BufferedReader(new FileReader(path))) {
            return r.readLine();
        }
    }

    public String join(List<String> xs) {
        String s = "";
        for (String x : xs) {
            s += x;                  // concatenation in a loop
        }
        return s;
    }
}

class Point {
    int x;
    public boolean equals(Object o) {   // no @Override and no hashCode
        return o instanceof Point && ((Point) o).x == x;
    }
}

class Good {
    int x;
    @Override
    public boolean equals(Object o) {
        return o instanceof Good && ((Good) o).x == x;
    }
    @Override
    public int hashCode() {
        return Integer.hashCode(x);
    }
}
