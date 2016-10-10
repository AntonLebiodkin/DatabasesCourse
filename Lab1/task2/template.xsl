<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>20 Sofas From meblium.com.ua</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th>Name</th>
      <th>Price</th>
      <th>Image</th>
      <th>Sizes</th>
    </tr>
    <xsl:for-each select="data/product">
    <tr>
        <td><xsl:value-of select="name"/></td>
        <td><xsl:value-of select="price"/></td>
        <td><img><xsl:attribute name="src">
            <xsl:value-of select="img"/>
        </xsl:attribute></img></td>
        <td><xsl:value-of select="sizes"/></td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>