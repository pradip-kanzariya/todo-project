import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("TODO")

# Create new todo
title = st.text_input("Title").strip()
description = st.text_input("Description")
create_button = st.button("CREATE")

if create_button and title:
    responce = requests.post(f"{BASE_URL}/todo/create", json={"title": title, "description": description})
    if responce.status_code == 200:
        st.success("Todo created!")
        st.rerun()
    else:
        st.error(responce.text)

# Track which todo is being edited
if "editing_id" not in st.session_state:
    st.session_state.editing_id = None

# Fetch todos
responce = requests.get(f"{BASE_URL}/todo")
if responce.status_code == 200:
    all_todos = responce.json()
    if all_todos:
        for todo in all_todos:
            with st.container():
                st.markdown(
                    f"### {todo['title']}\n"
                    f"{todo['description'] if todo['description'] else ''}"
                )

                col1, col2 = st.columns(2)

                # Edit button
                with col1:
                    if st.button("Edit", key=f"edit_{todo['id']}"):
                        st.session_state.editing_id = todo["id"]

                # Delete button
                with col2:
                    if st.button("Delete", key=f"delete_{todo['id']}"):
                        requests.delete(f"{BASE_URL}/todo/delete/{todo['id']}")
                        st.success("Todo deleted!")
                        st.rerun()

                # Show edit form if this todo is selected for editing
                if st.session_state.editing_id == todo["id"]:
                    new_title = st.text_input("New Title", value=todo["title"], key=f"title_{todo['id']}")
                    new_description = st.text_input("New Description", value=todo["description"], key=f"desc_{todo['id']}")
                    if st.button("Save", key=f"save_{todo['id']}"):
                        payload = {"title": new_title, "description": new_description}
                        edit_res = requests.patch(f"{BASE_URL}/todo/edit/{todo['id']}", json=payload)
                        if edit_res.status_code == 200:
                            st.success("Todo updated!")
                            st.session_state.editing_id = None
                            st.rerun()
                        else:
                            st.error(edit_res.text)
    else:
        st.write("No todos")
else:
    st.error(f"Error: {responce.text}")
