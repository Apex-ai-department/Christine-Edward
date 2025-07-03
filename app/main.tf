resource "aws_iam_policy" "ecr_pull" {
  name   = "ECRPullMyAppPolicy"
  policy = file("${path.module}/aws.json")
}