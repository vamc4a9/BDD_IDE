package GUI;

import javax.swing.*;
import javax.swing.border.Border;

import resources.test;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.net.URL;

public class ShowStepDefBeforeAdding extends JFrame implements ActionListener{
	private Container c;
	private JRadioButton JGiven, JWhen, JThen, JAnd; 
	private JTextField JStatement; 
	private ButtonGroup datagp; 
	private String sXMLPath, sXpath;
	private JButton jSubmit, JInfoIcon;
	private JTabbedPane editor;
	
	public ShowStepDefBeforeAdding(String sPath, String Statement, String xPath, JTabbedPane jTabPane) 
	{ 
		
		editor = jTabPane;
		sXMLPath = sPath;
		sXpath = xPath + "/StepDefinition[@Statement='" + Statement + "']";
		xml oXml = new xml();
		String Parameters = oXml.ReadAttribute(sPath, xPath 
				+ "/StepDefinition[@Statement='" + Statement + "']/@Parameters");

	    try {
	    	setContentPane(new JLabel(new ImageIcon(Toolkit.getDefaultToolkit().getImage(this.getClass().getResource("/resources/background_stepdef.jpg")))));
	    } catch (Exception e) {
	    	System.out.println(e.getMessage());
	    }
		setResizable(false);
		setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
		setTitle("Enter Details");
		setUndecorated(true);
		getRootPane().setWindowDecorationStyle(JRootPane.FRAME);
		Color TAborderColor = new Color(77, 166, 255);
		Color BtnBorderColor = new Color(255, 102, 0);
		c = getContentPane(); 
		c.setLayout(null);
		setLocationRelativeTo(null);
		JGiven = fn_AddRadioButton("Given", "Arial", 14, new Dimension(75, 20), new Point(50, 30), true);
		JWhen = fn_AddRadioButton("When", "Arial", 14, new Dimension(70, 20), new Point(125, 30), false);
		JThen = fn_AddRadioButton("Then", "Arial", 14, new Dimension(70, 20), new Point(195, 30), false);
		JAnd = fn_AddRadioButton("And", "Arial", 14, new Dimension(70, 20), new Point(265, 30), false);
		datagp = new ButtonGroup(); 
		datagp.add(JGiven);
		datagp.add(JWhen);
		datagp.add(JThen);
		datagp.add(JAnd);		
		
		JStatement = fn_AddTextField("Arial","StepDefStatement", 12, new Dimension(290, 20), new Point(50, 70), TAborderColor, Statement);
		
		int iInitY = 120; 
		if (!Parameters.contentEquals("")) {
			JInfoIcon = fn_AddIconButton("infoIcon.png", "Arial", 15, new Dimension(20, 20), new Point(360, 10));
			String[] sParameters = Parameters.split("\n");
			for (String param : sParameters) {
				String[] arParam = param.split("==");
				fn_AddTextLabel(arParam[0], arParam[1], "Arial", 14, new Dimension(100, 20), new Point(50, iInitY));
				fn_AddTextField("Arial", arParam[0], 14, new Dimension(150, 20), new Point(190, iInitY), TAborderColor, "");
				iInitY = iInitY + 40;
			}
		}
		
		jSubmit = fn_AddButton("Submit", "Arial", 15, new Dimension(100, 20), new Point(150, iInitY),BtnBorderColor);
		setSize(400, iInitY + 70);
		setVisible(true);
	}
	
	public JButton fn_AddButton(String sLabel, String sFont, int fSize, Dimension size, 
			Point iLocation, Color color) {
		
		c = getContentPane(); 
		JButton oButton = new JButton(sLabel); 
		oButton.setFont(new Font(sFont, Font.PLAIN, fSize)); 
		oButton.setSize(size); 
		oButton.setLocation(iLocation); 
		oButton.addActionListener(this);
		Border border = BorderFactory.createLineBorder(color, 2);
		oButton.setBorder(border);		
		c.add(oButton);
		return oButton;
		
	}		
	
	public JLabel fn_AddTextLabel(String sLabel, String sToolTip, String sFont, int fSize, Dimension size, 
			Point iLocation) {
		c = getContentPane(); 
		JLabel oTextLabel = new JLabel(sLabel); 
		oTextLabel.setFont(new Font(sFont, Font.PLAIN, fSize)); 
		oTextLabel.setToolTipText(sToolTip);
		oTextLabel.setSize(size); 
		oTextLabel.setLocation(iLocation); 
		oTextLabel.setName(sLabel);
		c.add(oTextLabel);
		return oTextLabel;
	}	
	
	public JRadioButton fn_AddRadioButton(String sLabel, String sFont, int fSize, Dimension size, 
			Point iLocation, boolean bSelected) {
		
		c = getContentPane(); 
		JRadioButton oRadioBtn = new JRadioButton(sLabel); 
		oRadioBtn.setFont(new Font(sFont, Font.PLAIN, fSize)); 
		oRadioBtn.setSelected(bSelected); 
		oRadioBtn.setOpaque(false);
		oRadioBtn.setSize(size); 
		oRadioBtn.setLocation(iLocation); 	
		c.add(oRadioBtn);
		return oRadioBtn;
	}
	
	public JTextField fn_AddTextField(String sFont, String sName, int fSize, Dimension size, 
			Point iLocation, Color color, String sDefaultText) {
		
		c = getContentPane(); 
		JTextField oTextField = new JTextField();
		oTextField.setFont(new Font(sFont, Font.PLAIN, fSize)); 
		oTextField.setSize(size); 
		oTextField.setLocation(iLocation); 
		Border border = BorderFactory.createLineBorder(color, 2);
		oTextField.setBorder(border);
		oTextField.setName(sName);
		oTextField.setText(sDefaultText);
		c.add(oTextField);
		
		return oTextField;
	}
	
	public void actionPerformed(ActionEvent e) 
	{ 
		if (e.getSource() == jSubmit) {
			String StepDefinitionStatement = ProcessStatement(getContentPane(), JStatement.getText());
			if (JGiven.isSelected())
				StepDefinitionStatement = "Given " + StepDefinitionStatement;
			else if (JWhen.isSelected())
				StepDefinitionStatement = "When " + StepDefinitionStatement;
			else if (JThen.isSelected())
				StepDefinitionStatement = "Then " + StepDefinitionStatement;
			else if (JAnd.isSelected())
				StepDefinitionStatement = "And " + StepDefinitionStatement;
            JTextArea oEditor = (JTextArea) editor.getSelectedComponent();
            oEditor.insert(StepDefinitionStatement, oEditor.getCaretPosition());
            oEditor.insert("\n", oEditor.getCaretPosition());
            dispose();
		} else if (e.getSource() == JInfoIcon) {
			msgbox("Hover on the parameter names to see the help information");
		}
	}
	
	public String ProcessStatement (Container parent, String Statement) {
	    for (Component c : parent.getComponents())
	    {
	    	if (c instanceof JTextField) {
	    		JTextField oField = (JTextField) c;
	    		if (!oField.getName().toLowerCase().contentEquals("StepDefStatement")) {
	    			if (!oField.getText().contentEquals(""))
	    				Statement = Statement.replace(oField.getName(), oField.getText());
	    		}
	    	}
	        if (c instanceof Container)
	        	ProcessStatement((Container)c, Statement);
	    }
	    return Statement;
	}

	public JButton fn_AddIconButton(String sImage, String sFont, int fSize, Dimension size, 
			Point iLocation) {
		
		test oTest = new test();
		c = getContentPane();
		URL imageURL = oTest.getClass().getResource(sImage);
		Icon icon = new ImageIcon(Toolkit.getDefaultToolkit().getImage(imageURL));
		JButton oButton = new JButton(icon);
		oButton.setFont(new Font(sFont, Font.PLAIN, fSize));
		oButton.setSize(size); 
		oButton.setOpaque(false);
		oButton.setFocusPainted(true);
		oButton.setBorderPainted(false);
		oButton.setContentAreaFilled(false);
		oButton.setBorder(BorderFactory.createEmptyBorder(0,0,0,0));
		oButton.setLocation(iLocation); 
		oButton.addActionListener(this);
		c.add(oButton);
		return oButton;
		
	}
	
	public void msgbox(String title) {
        JFrame oFrame = new JFrame("Message!");
        oFrame.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
        JOptionPane.showMessageDialog(oFrame,
        		title,
        	    "Message",
        	    JOptionPane.INFORMATION_MESSAGE);
	}
	
}