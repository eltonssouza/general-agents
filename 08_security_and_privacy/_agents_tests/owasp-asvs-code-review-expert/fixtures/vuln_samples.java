// Fixture derived from the OCRG examples (Samples 7.7, 16.1, 20.x); do not compile.
public class Demo {
  void a(HttpServletRequest request, HttpServletResponse response, Connection con, PrintWriter out) throws Exception {
    String userName = request.getParameter("name");
    String query = "SELECT * FROM Users WHERE name = '" + userName + "'";
    con.execute(query);
    response.sendRedirect(request.getParameter("url"));
    try { work(); } catch (Exception e) { e.printStackTrace(out); }
    try { work(); } catch (Throwable t) { }
    KeyGenerator keyGen = KeyGenerator.getInstance("DES");
    Cipher desCipher = Cipher.getInstance("DES/CBC/PKCS5Padding");
    MessageDigest md = MessageDigest.getInstance("MD5");
    logger.info("login ok user=" + user + " password=" + password);
    String password = "Sup3rS3cret!";
  }
  public native void nativeOp(byte[] data);
  private static String currentUser = null;
}
