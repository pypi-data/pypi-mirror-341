import powerbpy as PBI

import os

# Define file paths -----------------------------------------------------------------------------------------
report_name = "test_dashboard"
report_location = os.getcwd()

dashboard_path = os.path.join(report_location, report_name)



# Create a new dashboard -----------------------------------------------------------------------------------------
PBI_dash.create_new_dashboard(report_location, report_name)


# add data -------------------------------------------------------------------------------------------------------
# add locally stored csv files to the new dashboard
PBI.add_csv(dashboard_path, os.path.join(report_location, "powerbpy/examples/data/colony.csv" ))
PBI.add_csv(dashboard_path, os.path.join(report_location, "powerbpy/examples/data/wa_bigfoot_by_county.csv" ))

# add the default DateTable to the dashboard 
PBI.add_tmdl_dataset(dashboard_path = dashboard_path, data_path = None, add_default_datetable = True)



# add new page -----------------------------------------------------------------------------------------------------

## page 2 ---------------------------------------------------------------------------------------------------------
# create a new page
PBI.add_new_page(dashboard_path, 
	                   page_name = "Bee Colonies",
	                   title= "The bees are in Trouble!",
	                   subtitle = "We're losing bee colonies"
	)

# add background image
PBI.add_background_img(dashboard_path = dashboard_path, 
	               page_id = "page2", 
	               img_path = "./powerbpy/examples/data/Taipei_skyline_at_sunset_20150607.jpg", 
	               alpha = 51,
	               scaling_method = "Fit")

## page 3 ------------------------------------------------------------------------------------------------------
PBI.add_new_page(dashboard_path, 
	                   page_name = "Bigfoot Map",
	                   title= "Bigfoot sightings",
	                   subtitle = "By Washington Counties"
	)





# Add visual elements ---------------------------------------------------------------------------------------------------

# add a new column chart on the second page
PBI.add_chart(dashboard_path = dashboard_path, 
	      page_id = "page2", 
	      chart_id = "colonies_lost_by_year", 
	      chart_type = "columnChart",
	      data_source = "colony",
	      chart_title = "Number of Bee Colonies Lost per Year",
	      x_axis_title = "Year",
	      y_axis_title = "Number of Colonies",
	      x_axis_var = "year",
	      y_axis_var = "colony_lost",
	      y_axis_var_aggregation_type = "Sum",
	      x_position = 23,
	      y_position = 158,
	      height = 524,
	      width = 603)

# add a text box to the second page
PBI.add_text_box(text = "Explanatory text in the bottom right corner",
             dashboard_path= dashboard_path,
               page_id = "page2",
                 text_box_id = "page2_explain_box", 
                 height = 200,
                   width= 300,
                     x_position = 1000, 
                     y_position = 600, 
                     font_size = 15)

# add buttons

# download data button (a link to an internet address)
PBI.add_button(label = "Download Data",
  dashboard_path = dashboard_path,
  page_id = "page2",
  button_id = "page2_download_button",
  height = 40,
  width = 131,
  x_position = 1000,
  y_position = 540,
  url_link = "https://www.google.com/")

# navigate back to page 1 button
PBI.add_button(label = "Back to page 1",
  dashboard_path = dashboard_path,
  page_id = "page2",
  button_id = "page2_back_to_page1_button",
  height = 40,
  width = 131,
  x_position = 1000,
  y_position = 490,
  page_navigation_link = "page1")


## Add a map to page 3 ----------------------------------------------------------------------

PBI.add_shape_map(dashboard_path = dashboard_path, 
              page_id = "page3",
              map_id = "bigfoots_by_county_map",
              data_source = "wa_bigfoot_by_county",
              shape_file_path = "powerbpy/examples/data/2019_53_WA_Counties9467365124727016.json",
              
              map_title = "Washington State Bigfoot Sightings by County",
              #map_title = "",
              location_var = "county",
              color_var = "count",
              filtering_var = "season",
              #static_bin_breaks = [0, 15.4, 30.8, 46.2, 61.6, 77.0],
              percentile_bin_breaks = [0,0.2,0.4,0.6,0.8,1],
              color_palette = ["#efb5b9",  "#e68f96","#de6a73","#a1343c", "#6b2328"],
              height = 534,
              width = 816,
              x_position = 75,
              y_position = 132,
              z_position = 2000,
              add_legend = True
              #add_legend = False
              )





