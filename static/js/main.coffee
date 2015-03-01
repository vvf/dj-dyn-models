# here all logics

input_type_map =
  int:'<input type="number" name="{id}" value="{value}" class="vIntegerField">'
  char:'<input type="text" name="{id}" value="{value}" maxlength="255" class="vTextField">'
  date:'<input type="text" name="{id}" value="{value}" size="10" class="vDateField">'

date_re = /([0-9]{2})\.([0-9]{2})\.([0-9]{4})/
type_validators=
  int: (v)->
    parseInt(v) == v
  char: (v)->
    true
  date: (v)->
    a_date = date_re.exec(v)
    if not a_date
      return false
    try
      d_date = new Date(a_date[3], a_date[2]-1, a_date[1])
      return d_date.getDate() == a_date[1] and d_date.getMonth() == a_date[2]-1 and d_date.getFullYear() == a_date[3]
    catch
      return false

$=django.jQuery
$table_container = $('.table')
class Row
  delayed_save_timer: null
  constructor: (@model, @row_data)->
    @fields = $.extend {} , tables_meta_data[@model].fields
    @is_valid = yes
    yes

  delayed_save: ()->
    if @delayed_save_timer
      clearTimeout @delayed_save_timer
    self = @
    @delayed_save_timer = setTimeout ()->

      if self.is_valid
        self.startSaving()
    ,3000

  startSaving: ()->
    # start request to save.
    # if it calls til previous request is active - abort previous request and do a new
    console.log 'start saving', @row_data
    $td_id = @$row.find('td:first').html('Saving')
    self = @
    setTimeout ()->
      $td_id = self.row_data.id
    , 2500


  onChange: (inp)->
    name = $(inp).attr('name')
    is_valid = true
    for f in @fields
      if f.id == name
        val = $(inp).val()
        f.is_invalid = not type_validators[f.type](val)
        if not f.is_invalid
          @row_data[f.id] = val
      if f.is_invalid
        is_valid=false
    @is_valid = is_valid
    @delayed_save()

  get_table_row:()->
    header_html = ['<td>'+@row_data.id or ''+'</td>']
    for column in tables_meta_data[@model].fields
      input = input_type_map[column.type]
      column.value = @row_data[column.id] or ''
      for vname of column
        input = input.replace RegExp('{'+vname+'}', 'g'), column[vname]
      header_html.push "<td>"+input+"</td>"
    @$row = $("<tr class='row-#{@row_data.id}'>#{header_html.join('')}</tr>")
    self = @
    @$row.find('input').on 'change keyup blur', ()->
      self.onChange(@)

    return @$row

show_table=(model)->
  # render table, and make request
  header_html = ['<th>ID</th>']
  for column in tables_meta_data[model].fields
    header_html.push "<th>#{column.title}</th>"
  $table = $('<table></table>')

  $table.append '<tr>' + header_html.join('') + '</tr>'
  $table.append new Row(model,{id:'new'}).get_table_row()
  $table_container.html( $table )
  DateTimeShortcuts.init()

$model_menu = $ '.models-menu li'
$model_menu.find 'a'
  .on 'click touchstart', ()->
    $model_menu.removeClass 'active'
    $(@).closest('li').addClass 'active'
    show_table($(@).data('model'))
    false
