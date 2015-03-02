# here all logics

api_prefix=window.location.origin + '/api/'

input_type_map =
  int:'<input type="number" name="{id}" value="{value}" class="vIntegerField">'
  char:'<input type="text" name="{id}" value="{value}" maxlength="255" class="vTextField">'
  date:'<input type="text" name="{id}" value="{value}" size="10" class="vDateField">'

date_re = /([0-9]{2})\.([0-9]{2})\.([0-9]{4})/
numeric_RE = /^[0-9]+$/
type_validators=
  int: (v)->
    numeric_RE.test v
  char: (v)->
    true
  date: (v)->
    a_date = date_re.exec(v)
    if not a_date
      return false
    try
      d_date = new Date(a_date[3], a_date[2]-1, a_date[1])
      return d_date.getDate() == parseInt(a_date[1],10) and d_date.getMonth() == parseInt(a_date[2],10)-1 and d_date.getFullYear() == parseInt(a_date[3])
    catch
      return false

$=django.jQuery
$table_container = $('.table')
class Row
  delayed_save_timer: null
  constructor: (@model, @row_data, id=null, @$table)->
    @fields = []
    for f in tables_meta_data[@model].fields
      @fields.push f
    @row_data.id = id
    @last_data = $.extend({}, @row_data)
    @is_valid = yes
    @$table.append @get_table_row()

  delayed_save: ()->
    if @delayed_save_timer
      clearTimeout @delayed_save_timer
    self = @
    @delayed_save_timer = setTimeout ()->
      if self.is_valid
        self.startSaving()
    ,2000

  startSaving: ()->
    # start request to save.
    # if it calls til previous request is active - abort previous request and do a new
    console.log 'start saving', @row_data
    $td_id = @$row.find('td:first').html('Saving...') #TODO: here show image of saving animation
    self = @
    post_data = $.extend {csrfmiddlewaretoken:csrf_token, pk:@row_data.id}, @row_data
    $.post api_prefix+@model+'/', post_data, (result, status) ->
      result = JSON.parse result
      if result.success
        if not self.row_data.id
          new Row(self.model, {}, null, self.$table)
          self.$table.find('.datetimeshortcuts').remove()
          DateTimeShortcuts.init()

        self.row_data.id = result.row_id
        $td_id.html(self.row_data.id)
      else
        $td_id.html('saving error')


  onChange: (inp)->
    $inp = $(inp)
    name = $inp.attr('name')
    is_valid = yes
    has_changes = no
    for f in @fields
      if f.id == name
        val = $inp.val()
        f.is_invalid = not type_validators[f.type](val)
        if f.is_invalid
          $inp.addClass('error')
        else
          $inp.removeClass('error')
          @row_data[f.id] = val
      if f.is_invalid
        is_valid=false
      if @last_data[f.id] != @row_data[f.id]
        has_changes = yes
    @is_valid = is_valid
    if has_changes
      @delayed_save()

  get_table_row:()->
    row_id = @row_data.id or 'new'
    header_html = ['<td>' + row_id + '</td>']
    for column in tables_meta_data[@model].fields
      input = input_type_map[column.type]
      column.value = @row_data[column.id] or ''
      if column.type == 'date' and '-' in column.value
        column.value = column.value.split('-').reverse().join('.')
      for vname of column
        input = input.replace RegExp('{'+vname+'}', 'g'), column[vname]
      header_html.push "<td>"+input+"</td>"
    @$row = $("<tr class='row-#{row_id}'>#{header_html.join('')}</tr>")
    self = @
    @$row.find('input').on 'change blur', ()->
      self.onChange(@)

    return @$row

show_table=(model)->
  # render table, and make request
  header_html = ['<th>ID</th>']
  for column in tables_meta_data[model].fields
    header_html.push "<th>#{column.title}</th>"
  $table = $('<table></table>')
  $table.append '<tr>' + header_html.join('') + '</tr>'
  $new = new Row(model, {}, null, $table)
  $.get api_prefix+model, (data, status)->
    row_data = JSON.parse(data)
    for row in row_data
      new Row(model, row.fields, row.pk, $table)
    $table.append $new.$row
    $table.find('.datetimeshortcuts').remove()
    DateTimeShortcuts.init()

  $table_container.html( $table )
  DateTimeShortcuts.init()

$model_menu = $ '.models-menu li'
$model_menu.find 'a'
  .on 'click touchstart', ()->
    $model_menu.removeClass 'active'
    $(@).closest('li').addClass 'active'
    show_table($(@).data('model'))
    false

csrf_token = $('.table input[name=csrfmiddlewaretoken]').val()