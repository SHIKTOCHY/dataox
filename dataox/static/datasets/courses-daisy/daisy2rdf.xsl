<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:html="http://www.w3.org/1999/xhtml#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:skos="http://www.w3.org/2004/02/skos/core#"
    xmlns:gr="http://purl.org/goodrelations/v1#"
    xmlns:event="http://purl.org/NET/c4dm/event.owl#"
    xmlns:prog="http://purl.org/prog/"
    xmlns:tl="http://purl.org/NET/c4dm/timeline.owl#"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:mlo="http://purl.org/net/mlo/"
    xmlns:xcri="http://xcri.org/profiles/1.2/"
    xmlns:daisy="http://daisy.socsci.ox.ac.uk/ns/"
    xmlns="http://xcri.org/profiles/1.2/catalog"
    xpath-default-namespace="http://xcri.org/profiles/1.2/catalog">
  <xsl:import href="xcri2rdf.xsl"/>
  <xsl:output method="xml" indent="yes"/>

  <xsl:param name="store">public</xsl:param>

  <xsl:variable name="base">https://course.data.ox.ac.uk/id/daisy/</xsl:variable>
  <xsl:variable name="publisher-uri">http://oxpoints.oucs.ox.ac.uk/id/23232714</xsl:variable>

  <xsl:template match="catalog" mode="rdf-about">
    <xsl:value-of select="concat($base, 'catalogue')"/>
  </xsl:template>

  <xsl:template match="course" mode="in-catalog">
    <xsl:if test="$store='courses' or not(daisy:publicView/text()='0')">
      <xsl:apply-imports/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="course" mode="rdf-about">
    <xsl:value-of select="concat($base, 'course/', dc:identifier[@daisy:type='assessmentUnitId']/text())"/>
  </xsl:template>

  <xsl:template match="presentation" mode="rdf-about">
    <xsl:value-of select="concat($base, 'presentation/', dc:identifier/text())"/>
  </xsl:template>
</xsl:stylesheet>