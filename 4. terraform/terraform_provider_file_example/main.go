package main

import (
	"github.com/hashicorp/terraform-plugin-sdk/v2/plugin"
	"terraform_provider_file_example/sample_file_provider"
)

func main() {
	opts := &plugin.ServeOpts{ProviderFunc: sample_file_provider.Provider}
	plugin.Serve(opts)
}
