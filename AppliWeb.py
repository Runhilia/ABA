from ABA import ABA
from Parser import Parser
import streamlit as st

def print_attacks(attacks):
    code =""
    for att in attacks:
        code += "{"
        for i, subset in enumerate(att[0]):
            code += subset.to_string()
            if i < len(att[0]) - 1:
                code += ","
        code += "} -> {"
        for i, subset in enumerate(att[1]):
            code += subset.to_string()
            if i < len(att[1]) - 1:
                code+= "," 
        code += "}\n"
        
    return code


if __name__ == "__main__":
    st.title("Dynamique des Connaissances Project")
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        parser = Parser(uploaded_file.name)
        aba = ABA(parser.L, parser.R, parser.A, parser.C, parser.P)
        
        for rel in aba.P:
            print(rel.to_string())
        
        st.subheader("ABA basic :")
        st.code(aba, language="python")
        
        with st.expander("Expected"):
            if(uploaded_file.name == "example1.txt"):
                st.image("./Images/framework1.png")
            else:
                st.text("No data available")
            
        
        
        st.text("Is the framework atomic ? " + str(aba.is_atomic()))
        st.text("Is the framework circular ? " + str(aba.is_circular()))
        
        with st.expander("Expected"):
            if(uploaded_file.name == "example1.txt"):
                st.text("The ABA framework is not circular and not atomic")
            else:
                st.text("No data available")
        
        aba.create_non_cicular()
        st.subheader("ABA non circular :")
        st.code(aba, language="python")
        
        with st.expander("Expected"):
            if(uploaded_file.name == "example1.txt"):
                st.image("./Images/framework1.png")
            else:
                st.text("No data available")
        
        st.subheader("List of rules :")
        code = ""
        for rule in aba.R:
            code += rule.to_string() + "\n"
        st.code(code, language="python")
        
        st.subheader("List of arguments :")
        args = aba.create_argument()
        code = ""
        for argument in args:
            code += argument.to_string() + "\n"
        st.code(code, language="python")
        st.text("Number of arguments : " + str(len(args)))
        
        with st.expander("Expected"):
            if(uploaded_file.name == "example1.txt"):
                st.image("./Images/arguments1.png")
            else:
                st.text("No data available")
        
        
        st.subheader("List of attacks :")
        att = aba.create_attacks(args)
        code = ""
        for attack in att:
            code += attack[0].get_name() + " -> " + attack[1].get_name() + "\n"
        st.code(code, language="python")
        st.text("Number of attacks : " + str(len(att)))
        
        with st.expander("Expected"):
            if(uploaded_file.name == "example1.txt"):
                st.image("./Images/attacks1.png")
            else:
                st.text("No data available")
                
        st.subheader("Normal attacks :")
        normal_att = aba.create_normal_attacks(args)
        code = print_attacks(normal_att)
        st.code(code, language="python")
        st.text("Number of normal attacks : " + str(len(normal_att)))
                
        with st.expander("Expected"):
            if(uploaded_file.name == "example1.txt"):
                st.image("./Images/normalAttacks1.png")
            else:
                st.text("No data available")
        
        st.subheader("Reverse attacks :")
        reverse_att = aba.create_reverse_attacks(args)
        code = print_attacks(reverse_att)
        st.code(code, language="python")
        st.text("Number of reverse attacks : " + str(len(reverse_att)))
        
        with st.expander("Expected"):
            if(uploaded_file.name == "example1.txt"):
                st.image("./Images/reverseAttacks1.png")
            else:
                st.text("No data available")
        
        
        st.subheader("ABA non-circular and atomic :")
        aba.non_circular_into_atomic()
        st.code(aba, language="python")
        
        with st.expander("Expected"):
            if(uploaded_file.name == "example1.txt"):
                st.text("No data available")
            else:
                st.text("No data available")
                
        
        
        