def load_components_responses():
	return {
		'RolesResponse':              {
			'type':       'object',
			'properties': {
				'roles': {
					'type':  'array',
					'items': {
						'type': 'string'
						}
					}
				}
			},
		'AuthorizationErrorResponse': {
			'type':       'object',
			'properties': {
				'error':       {
					'type':    'string',
					'default': 'MissingToken'
					},
				'message':     {
					'type':    'string',
					'default': "Could not find token in any of the given "
					           "locations: ['header', 'cookie']"
					},
				'status_code': {
					'type':    'integer',
					'default': 401
					}
				}
			}
		, 'ItemGetResponse':          {
			'type':       'object',
			'properties': {
				'category_id':           {
					'type': 'integer'
					},
				'item_cost':             {
					'type': 'integer'
					},
				'item_description':      {
					'type': 'string'
					},
				'item_id':               {
					'type': 'integer'
					},
				'item_name':             {
					'type': 'string'
					},
				'item_quantity_current': {
					'type': 'integer'
					},
				'item_quantity_max':     {
					'type': 'integer'
					},
				'item_weight':           {
					'type': 'integer'
					}
				}
			},
		'ListItemsGetResponse':       {
			'type':       'object',
			'properties': {
				'items': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/ItemGetResponse'
						}
					}
				}
			},
		'ItemInUseResponse':          {
			'type':       'object',
			'properties': {
				'is_confirm':      {
					'type': 'boolean'
					},
				'item_id':         {
					'type': 'integer'
					},
				'item_quantity':   {
					'type': 'integer'
					},
				'until_datetime':  {
					'type': 'string'
					},
				'use_datetime':    {
					'type': 'string'
					},
				'use_description': {
					'type': 'string'
					},
				'user_id':         {
					'type': 'integer'
					},
				'use_id':          {
					'type': 'integer'
					},
				'warehouseman_id': {
					'type': 'integer'
					}
				}
			},
		'ListItemInUseResponse':      {
			'type':       'object',
			'properties': {
				'items': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/ItemInUseResponse'
						}
					}
				}
			},
		'UserDataResponse':           {
			'type':       'object',
			'properties': {
				'user': {
					'type':       'object',
					'properties': {
						"user_email":    {
							'type': 'string'
							},
						"user_id":       {
							'type': 'integer'
							},
						"user_isactive": {
							'type': 'integer'
							},
						"user_login":    {
							'type': 'string'
							},
						"user_money":    {
							'type': 'integer'
							},
						"user_name":     {
							'type': 'string'
							},
						"user_phone":    {
							'type': 'string'
							},
						"user_roles":    {
							'type':  'array',
							'items': {
								'type': 'string'
								}
							}
						}
					}
				}
			},
		'UserDataItemsResponse':      {
			'type':       'object',
			'properties': {
				'user': {
					'type':       'object',
					'properties': {
						"user_email":    {
							'type': 'string'
							},
						"user_id":       {
							'type': 'integer'
							},
						"user_isactive": {
							'type': 'integer'
							},
						"user_login":    {
							'type': 'string'
							},
						"user_money":    {
							'type': 'integer'
							},
						"user_name":     {
							'type': 'string'
							},
						"user_phone":    {
							'type': 'string'
							},
						"user_roles":    {
							'type':  'array',
							'items': {
								'type': 'string'
								}
							},
						'items':         {
							'type':  'array',
							'items': {
								'$ref':
									'#/components/schemas/ItemInUseResponse'
								}
							}
						}
					}
				}
			},
		'ListUserDataResponse':       {
			'type':       'object',
			'properties': {
				'users': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/UserDataResponse'
						}
					}
				}
			},

		'AccessTokenResponse':        {
			'type':       'object',
			'properties': {
				'access_token': {
					'type': 'string'
					}
				}
			},
		'SignupResponse':             {
			'type':       'object',
			'properties': {
				"signup_datetime": {
					'type': "string"
					}
				,
				"signup_id":       {'type': "integer"},
				"user_email":      {'type': "string"},
				"user_login":      {'type': "string"},
				"user_name":       {'type': "string"},
				"user_phone":      {'type': "string"}
				}
			},
		'ListSignupResponses':        {
			'type':       'object',
			'properties': {
				'requests': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/SignupResponse'
						}
					}
				}
			},
		'CategoryResponse':           {
			'type':       'object',
			'properties': {
				# 'category_datetime': {'type': 'string'},
				'category_id':     {'type': 'integer'},
				'category_name':   {'type': 'string'},
				'category_weight': {'type': 'integer'}
				}
			},
		'ListCategoryResponses':      {
			'type':       'object',
			'properties': {
				'categories': {
					'type':  'array',
					'items': {'$ref': '#/components/schemas/CategoryResponse'}
					}
				}
			},
		'CategoryAndItemsResponse':   {
			'type':       'object',
			'properties': {
				'category_id':     {'type': 'integer'},
				'category_name':   {'type': 'string'},
				'category_weight': {'type': 'integer'},
				'items':           {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/ItemGetResponse'
						}
					}
				}
			},
		'MoneyHistoryResponse':       {
			'type':       'object',
			'properties': {
				'history_id':       {'type': 'integer'},
				'user_id':          {'type': 'integer'},
				'auser_id':         {'type': 'integer'},
				'old_value':        {'type': 'integer'},
				'new_value':        {'type': 'integer'},
				'history_datetime': {'type': 'string'}
				}
			},
		'ListMoneyHistoryResponse':{
			'type':'object',
			'properties':{
				'list':{
					'type':'array',
					'items':{
						'$ref':'#/components/schemas/MoneyHistoryResponse'
						}
					}
				}
			}
		}


def load_components_requests():
	return {
		'CreateItemRequest':      {
			'type':       'object',
			'properties': {
				'name':        {
					'type': 'string'
					},
				'category_id': {
					'type': 'integer'
					},
				'weight':      {
					'type': 'integer'
					},
				'quantity':    {
					'type': 'integer'
					},
				'cost':        {
					'type': 'integer'
					},
				'description': {
					'type': 'string'
					}
				# image?
				}
			},
		'ChangeItemDataRequest':  {
			'type':       'object',
			'properties': {
				'name':        {
					'type': 'string'
					},
				'category_id': {
					'type': 'integer'
					},
				'weight':      {
					'type': 'integer'
					},
				'quantity':    {
					'type': 'integer'
					},
				'cost':        {
					'type': 'integer'
					},
				'description': {
					'type': 'string'
					}
				# image?
				}
			},
		'ItemIdRequest':          {
			'type': 'integer'
			},
		'ItemQuantityRequest':    {
			'type': 'integer'
			},
		'BookItemRequest':        {
			'type':       'object',
			'properties': {
				'item_id':       {
					'type': 'integer'
					},
				'quantity':      {
					'type': 'integer'
					},
				'datetime_from': {
					'type': 'string'
					},
				'datetime_to':   {
					'type': 'string'
					}
				}
			},
		'ListBookItemsRequest':   {
			'type':       'object',
			'properties': {
				'items': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/BookItemRequest'
						}
					}
				}
			},
		'UseIdRequest':           {
			'type':       'object',
			'properties': {
				'use_id':   {
					'$ref': '#/components/schemas/IdRequest'
					},
				'quantity': {
					'type': 'integer'
					}
				}
			},
		'ListUseIdRequest':       {
			'type':       'object',
			'properties': {
				'use_ids': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/UseIdRequest'
						}
					}
				}
			},
		'ApproveItemRequest':     {
			'type':       'object',
			'properties': {
				'description': {
					'type': 'string'
					},
				'use_id':      {
					'type': 'integer'
					}
				}
			},
		'ListApproveItemRequest': {
			'type':       'object',
			'properties': {
				'use_ids': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/ApproveItemRequest'
						}
					}
				}
			},
		'IdRequest':              {
			'type': 'integer'
			},
		'GiveRequest':            {
			'type':       'object',
			'properties': {
				'use_id': {
					'type': 'integer'
					},
				'days':   {
					'type': 'integer'
					}
				}
			},
		'ListGiveRequest':        {
			'type':       'object',
			'properties': {
				'use_ids': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/GiveRequest'
						}
					}
				}
			},
		'ListRejectItemRequest':  {
			'type':       'object',
			'properties': {
				'use_ids': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/IdRejectRequest'
						}
					}
				}
			},
		'ListGiveItemRequest':    {
			'type':       'object',
			'properties': {
				'use_ids': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/IdRequest'
						}
					}
				}
			},
		'QuantityIdRequest':      {
			'type':       'object',
			'properties': {
				'use_id':      {
					'$ref': '#/components/schemas/IdRequest'
					},
				'quantity':    {
					'type': 'integer'
					},
				'description': {
					'type': 'string'
					}
				}
			},
		'ListQuantityIdRequest':  {
			'type':       'object',
			'properties': {
				'use_ids': {
					'type':  'array',
					'items': {
						'$ref': '#/components/schemas/QuantityIdRequest'
						}
					}
				}
			},
		'ChangePasswordRequest':  {
			'type':       'object',
			'properties': {
				'old_password': {
					'type': 'string'
					},
				'new_password': {
					'type': 'string'
					}
				}
			},
		'NewEmailRequest':        {
			'type':       'object',
			'properties': {
				'new_email': {
					'type': 'string'
					}
				}
			},
		'NewLoginRequest':        {
			'type':       'object',
			'properties': {
				'new_login': {
					'type': 'string'
					}
				}
			},

		'NewUsernameRequest':     {
			'type':       'object',
			'properties': {
				'new_username': {
					'type': 'string'
					}
				}
			},

		'NewPhoneRequest':        {
			'type':       'object',
			'properties': {
				'new_phone': {
					'type': 'string'
					}
				}
			},
		'SignupRequest':          {
			'type':       'object',
			'properties': {
				'login':    {
					'type': 'string'
					},
				'email':    {
					'type': 'string'
					},
				'name':     {
					'type': 'string'
					},
				'phone':    {
					'type': 'string'
					},
				'password': {
					'type': 'string'
					}
				}
			},
		'TokenConfirmRequest':    {
			'type': 'string'
			},
		'LoginRequest':           {
			'type':       'object',
			'properties': {
				'login':    {
					'type': 'string'
					},
				'password': {
					'type': 'string'
					}
				}
			},
		'EmailRequest':           {
			'type':       'object',
			'properties': {
				'email': {
					'type': 'string'
					}
				}
			},
		'PasswordRequest':        {
			'type':       'object',
			'properties': {
				'password': {
					'type': 'stringF'
					}
				}
			},
		'SignupIdRequest':        {
			'type': 'integer'
			},
		'ListOnlyUseIdRequest':   {
			'type':       'object',
			'properties': {
				'use_ids': {
					'type':  'array',
					'items': {
						'type':       'object',
						'properties': {
							'use_id': {
								'$ref': '#/components/schemas/IdRequest'
								}
							}
						}
					}
				}
			}
		, 'CreateUserRequest':    {
			'type':       'object',
			'properties': {
				'login':    {
					'type': 'string'
					},
				'password': {
					'type': 'string'
					},
				'name':     {
					'type': 'string'
					},
				'email':    {
					'type': 'string'
					},
				'phone':    {
					'type': 'string'
					}
				}
			},
		'UsernameRequest':        {
			'type':       'object',
			'properties': {
				'username': {
					'type': 'string'
					}
				}
			},
		'UserDataRequest':        {
			'type':       'object',
			'properties': {
				'user': {
					'type':       'object',
					'properties': {
						"email":     {
							'type': 'string'
							},
						"is_active": {
							'type': 'integer'
							},
						"login":     {
							'type': 'string'
							},
						"money":     {
							'type': 'integer'
							},
						"name":      {
							'type': 'string'
							},
						"phone":     {
							'type': 'string'
							},
						"roles":     {
							'type':  'array',
							'items': {
								'type': 'string'
								}
							},
						'password':  {
							'type': 'string'
							}
						}
					}
				}
			},
		'ListDaysUseIdRequest':   {
			'type':       'object',
			'properties': {
				'use_ids': {
					'type':  'array',
					'items': {
						'type':       'object',
						'properties': {
							'use_id': {
								'type': 'integer'
								},
							'days':   {
								'type': 'integer'
								}
							}
						}
					}
				}
			},
		'IdRejectRequest':        {
			'type':       'object',
			'properties': {
				'use_id':      {
					'type': 'integer'
					},
				'description': {
					'type': 'string'
					}
				}
			},
		'CreateCategoryRequest':  {
			'type':       'object',
			'properties': {
				'category_name':   {'type': 'string'},
				'category_weight': {'type': 'integer'}
				}
			}
		}
