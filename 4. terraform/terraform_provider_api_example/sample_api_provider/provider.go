package sample_api_provider

import "github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"

// Provider This is the entrypoint for the provider
func Provider() *schema.Provider {
	return &schema.Provider{
		Schema: map[string]*schema.Schema{
			"car_api_url": {
				Type:        schema.TypeString,
				Required:    true,
				DefaultFunc: schema.EnvDefaultFunc("CAR_API_URI", nil),
				Description: "The URL of the API to use for the car resource",
			},
		},
	}
}
