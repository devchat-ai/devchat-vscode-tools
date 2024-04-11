(class_declaration
  (initializer_declaration
    parameter_clause: (parameter_clause
      parameter_list: (parameter_list
        parameter: (parameter
          local_name: (identifier) @variable
        )
      )
    )
  )
)

(function_declaration
  parameter_clause: (parameter_clause
    parameter_list: (parameter_list
      parameter: (parameter
        local_name: (identifier) @variable
      )
    )
  )
)

(variable_declaration
  name: (identifier) @variable
)

(tuple_type
  element_list: (tuple_type_element_list
    element: (tuple_type_element
      name: (identifier) @variable
    )
  )
)
