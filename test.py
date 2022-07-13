



# in our program we will want entities
#   entities are nothing more than an ID number
# we will also have components
#   each component is just a dictionary of information
#   we will need a table for each component
#       the table has a primary key of the entity ID number, then values for each of the component parts
# 
# we will have a system for each action that can be taken
#   this will collect actions throughout the gameloop
#   each system is responsible for 1 action (though we can potentially group them together in)
#   the actions should contain nothing more than a reference to the entity ID
#   the system will iterate over all the entities that have flagged they need to do something

