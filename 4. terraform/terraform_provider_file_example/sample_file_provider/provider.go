package sample_file_provider

import (
	"context"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/hashicorp/terraform-plugin-sdk/v2/diag"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

// Provider is what it sounds like
func Provider() *schema.Provider {
	p := &schema.Provider{
		Schema: map[string]*schema.Schema{
			"directory": {
				Type:     schema.TypeString,
				Required: true,
			},
		},
		DataSourcesMap: map[string]*schema.Resource{
			"file_data_source": dataSourceFile(),
		},
		ResourcesMap: map[string]*schema.Resource{
			"file_resource": resourceFile(),
		},
	}

	p.ConfigureContextFunc = configure

	return p
}

func configure(ctx context.Context, d *schema.ResourceData) (interface{}, diag.Diagnostics) {
	directory := d.Get("directory").(string)

	return &fileClient{
		directory: directory,
	}, nil
}

type fileClient struct {
	directory string
}

func (f *fileClient) write(filename, content string) error {
	file, err := os.Create(fmt.Sprintf("%s/%s", f.directory, filename))
	if err != nil {
		return err
	}

	_, err = file.WriteString(content)
	return err
}

func (f *fileClient) read(filename string) (string, error) {
	file, err := os.Open(fmt.Sprintf("%s/%s", f.directory, filename))
	if err != nil {
		return "", err
	}
	content, err := ioutil.ReadAll(file)
	return string(content), err
}

func (f *fileClient) delete(filename string) error {
	return os.Remove(fmt.Sprintf("%s/%s", f.directory, filename))
}
