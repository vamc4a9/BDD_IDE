package GUI;

import java.io.File;

import javax.swing.JTree;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathFactory;

import org.dom4j.DocumentException;
import org.dom4j.io.SAXReader;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class xml {

	public Document GetDocumentFromXml(String xmlPath) {
		try {
			DocumentBuilderFactory oDoc = DocumentBuilderFactory.newInstance();
			DocumentBuilder db = oDoc.newDocumentBuilder();
			Document doc = null;
			doc = db.parse(xmlPath);
			
			return doc;
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
	
	public String ReadAttribute(String xmlPath, String xPath) {
		NodeList node;
		try {
			Document doc = GetDocumentFromXml(xmlPath);
			XPathFactory xpathFactory = XPathFactory.newInstance();
			XPath xpath = xpathFactory.newXPath();
			XPathExpression expr = xpath.compile(xPath);
			node = (NodeList) expr.evaluate(doc, XPathConstants.NODESET);
			Node oEle = node.item(0);
			return oEle.getTextContent();
		} catch (Exception e) {
			return "";
		}
	}
	
	public void UpdateXml(String xmlPath, String xPath, String sValue) {
		NodeList node;
		try {
			Document doc = GetDocumentFromXml(xmlPath);
			XPathFactory xpathFactory = XPathFactory.newInstance();
			XPath xpath = xpathFactory.newXPath();
			XPathExpression expr = xpath.compile(xPath);
			node = (NodeList) expr.evaluate(doc, XPathConstants.NODESET);
			Node oEle = node.item(0);
			oEle.setTextContent(sValue);
			Transformer transformer = TransformerFactory.newInstance().newTransformer();
			transformer.transform(new DOMSource(doc), new StreamResult(new File(xmlPath)));			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public void RemoveFromXml(String xmlPath, String xPath) {
		NodeList node;
		try {
			Document doc = GetDocumentFromXml(xmlPath);
			XPathFactory xpathFactory = XPathFactory.newInstance();
			XPath xpath = xpathFactory.newXPath();
			XPathExpression expr = xpath.compile(xPath);
			node = (NodeList) expr.evaluate(doc, XPathConstants.NODESET);
			Node oEle = node.item(0);
			oEle.getParentNode().removeChild(oEle);
			Transformer transformer = TransformerFactory.newInstance().newTransformer();
			transformer.transform(new DOMSource(doc), new StreamResult(new File(xmlPath)));
	
		} catch (Exception e) {
			e.printStackTrace();
		}
	}	
	
	public void AddToXml(String xmlPath, String xPath, String statement, String xtrnlData, String sInstructions) {
		NodeList node;
		try {
			Document doc = GetDocumentFromXml(xmlPath);
			XPathFactory xpathFactory = XPathFactory.newInstance();
			XPath xpath = xpathFactory.newXPath();
			XPathExpression expr = xpath.compile(xPath);
			node = (NodeList) expr.evaluate(doc, XPathConstants.NODESET);
			Node oEle = node.item(0);
			Element newElement = doc.createElement("StepDefinition");
			newElement.setAttribute("Statement", statement);
			newElement.setAttribute("ExternalData", xtrnlData);
			newElement.setAttribute("Instructions", sInstructions);
			oEle.appendChild(newElement);
			Transformer transformer = TransformerFactory.newInstance().newTransformer();
			transformer.transform(new DOMSource(doc), new StreamResult(new File(xmlPath)));
		} catch (Exception e) {
			
		}
		
		
		
	}

	
}
