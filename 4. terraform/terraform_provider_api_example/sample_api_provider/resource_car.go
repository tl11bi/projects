package sample_api_provider

import (
	"context"
	"github.com/hashicorp/terraform-plugin-sdk/v2/diag"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

func resourceCar() *schema.Resource {
	return &schema.Resource{
		Description:   "A car.",
		CreateContext: resourceCarCreate,
		ReadContext:   resourceCarRead,
		UpdateContext: resourceCarUpdate,
		DeleteContext: resourceCarDelete,
		Schema: map[string]*schema.Schema{
			"color": {
				Description: "The color of the car",
				Type:        schema.TypeString,
				Required:    true,
			},
			"make": {
				Description: "The make of the car",
				Type:        schema.TypeString,
				Required:    true,
			},
			"model": {
				Description: "The model of the car",
				Type:        schema.TypeString,
				Required:    true,
			},
			"year": {
				Description: "The year of the car",
				Type:        schema.TypeInt,
				Required:    true,
			},
			"description": {
				Description: "The description of the car",
				Type:        schema.TypeString,
				Required:    false,
			},
		},
	}
}

func resourceCarCreate(ctx context.Context, d *schema.ResourceData, m interface{}) diag.Diagnostics {
	// send a post request to the api to create a car with the given data in the schema
	var err error
	if content, ok :=
	return nil


}
