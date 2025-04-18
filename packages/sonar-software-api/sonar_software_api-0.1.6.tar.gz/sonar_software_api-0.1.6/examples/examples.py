import Sonar

sonar = Sonar("SONAR_URL", "API_TOKEN")


#Query
query = """{
          accounts{
            entities{
              id
              name
              }
            }
          }"""

accounts = sonar.graphql(query, variable_values=None)
