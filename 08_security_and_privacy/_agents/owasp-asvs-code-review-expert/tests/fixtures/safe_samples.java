// Safe fixture (OCRG Sample 7.1): parameterized query
public class Safe {
  void a(Connection connection, String firstname, String lastname) throws Exception {
    String query = "SELECT id, firstname, lastname FROM authors WHERE forename = ? and surname = ?";
    PreparedStatement pstmt = connection.prepareStatement(query);
    pstmt.setString(1, firstname);
    pstmt.setString(2, lastname);
    String sql = "select id from authors" + " where forename = ?";
    try { work(); } catch (IOException e) { logger.log(Level.SEVERE, "failure", e); }
    MessageDigest md = MessageDigest.getInstance("SHA-256");
  }
}
