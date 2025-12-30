# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f"Example Streamlit App :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie
  """
)
name_of_order = st.text_input('Name on Smoothie: ')
st.write('the name on your Smoothie will be: '+name_of_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect("chose up to 5 ingredients"
                                  ,my_dataframe
                                  ,max_selections=5
                                 )

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    st.write(ingredients_string)

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_of_order +  """')"""

    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit order')
    #st.stop()
    if time_to_insert:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
    
    

