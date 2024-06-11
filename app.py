import streamlit as st
import numpy as np
from sympy import Matrix, symbols

def create_hessian_matrix(n, m):
    matrix = np.zeros((n, m))
    b = np.zeros(n)
    for i in range(n):
        st.write(f"Entrez les éléments de la ligne {i + 1} de la matrice hessienne:")
        for j in range(m):
            matrix[i][j] = st.number_input(f"Element {j + 1} :", key=f"{i}-{j}", step=0.5)
    # read b values:
    st.write("Entrer les valeurs du vecteur b: ")
    b = [st.number_input(f"b[{i + 1}] = ") for i in range(n)]

    return matrix, b

def solve_system(hessian_matrix, b):
    try:
        solution = np.linalg.solve(hessian_matrix, b)
        return tuple(solution)
    except Exception as e:
        st.error(f"Erreur lors du calcul de la solution : {e}")
        return None

def polynome_caracteristique(matrice):
    matrice_sympy = Matrix(matrice)
    lambda_sym = symbols('lambda')
    # Calculer le polynôme caractéristique
    polynome = matrice_sympy.charpoly(lambda_sym).as_expr()
    # Calculer les valeurs propres
    valeurs_propres = np.linalg.eigvals(matrice)
    
    return polynome, valeurs_propres


def display_result_page():
    st.sidebar.title("Programmation quadratique Application")
    st.sidebar.markdown("---")
    st.title("Display Results Page: ")
    if st.session_state.hessian_matrix is None or st.session_state.b is None:
        st.info("Merci de saisir les données avant de tester.")
        return
    # Afficher la matrice depuis la session
    st.write("Matrice Hessienne saisie H:")
    st.write(np.array(st.session_state.hessian_matrix))
    st.write(f"Le vecteur b = {tuple([i for i in st.session_state.b])}")
    # Affichage du résultat
    st.write("Polynôme caractéristique :", st.session_state.polynome)
    st.write("Valeurs propres associées :", st.session_state.valeurs_propres)
    n, m = st.session_state.hessian_matrix.shape
    # Tester les valeurs propres
    if all(val > 0 for val in st.session_state.valeurs_propres):
        st.success("Toutes les valeurs propres sont strictement positives. La fonction est strictement convexe, "
                "admet un unique minimum global, et la solution unique du système HX = b est le minimum global.")
        # Calculer la solution du système HX = b
        solution = solve_system(st.session_state.hessian_matrix, st.session_state.b)
        if solution is not None:
            st.write(f"La solution du système HX = b est : {solution}")
    elif all(val < 0 for val in st.session_state.valeurs_propres):
        st.success("Toutes les valeurs propres sont strictement négatives. La fonction est strictement concave, "
                "admet un unique maximum global.")
        solution = solve_system(st.session_state.hessian_matrix, st.session_state.b)
        if solution is not None:
            st.write(f"La solution du système HX = b est : {solution}")
    else:
        st.warning("Les valeurs propres ne sont pas toutes strictement positives ni toutes strictement négatives. "
                "La nature de la fonction n'est pas déterminée uniquement par le test sur les valeurs propres.")

def input_page():
    st.title("Page de Saisie des Paramètres :")
    st.sidebar.title("Programmation quadratique Application")
    st.sidebar.markdown("---")
    st.write("La Matrice Hessienne : ")
    n = st.number_input("Nombre de lignes:", min_value=2, step=1)
    m = st.number_input("Nombre de colonnes:", min_value=2, step=1)
    hessian_matrix, b = create_hessian_matrix(int(n), int(m))
    if st.button("Valider"):
        st.session_state.hessian_matrix = hessian_matrix
        st.session_state.b = b
        try:
            polynome, valeurs_propres = polynome_caracteristique(hessian_matrix.tolist())
            st.session_state.polynome = polynome
            st.session_state.valeurs_propres = valeurs_propres
            st.success("Les données saisies sont correctes.")
            st.info("Cliquez sur 'Display Results' ci-dessus pour voir les résultats.")
        except Exception as e:
            st.error(f"Erreur : {e}")


def main():
    # Déclarer la session_state pour stocker les parametres
    if "hessian_matrix" not in st.session_state:
        st.session_state.hessian_matrix = None
    if "b" not in st.session_state:
        st.session_state.b = None
    if "polynome" not in st.session_state:
        st.session_state.polynome = None
    if "valeurs_propres" not in st.session_state:
        st.session_state.valeurs_propres = None
    # Utiliser les pages pour gérer la navigation   
    pages = {"Enter Parameters": input_page, "Display Results": display_result_page}
    current_page = st.radio("Options : ", list(pages.keys()))
    # Afficher la page actuelle
    pages[current_page]()

main()
    