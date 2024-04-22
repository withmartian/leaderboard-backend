resource "aws_scheduler_schedule" "daily_collections" {
  name = "${var.service}-daily-collections-${var.env}"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(6 hours)"

  target {
    arn      = aws_sqs_queue.daily_collections.arn
    role_arn = aws_iam_role.daily_collections_scheduler_role.arn

    input = jsonencode({
      "type" : "DailyCollections",
      "timestamp" : 0,
      "data" : {}
    })
  }
}

resource "aws_iam_role" "daily_collections_scheduler_role" {
  name = "${var.service}-daily-collections-scheduler-role-${var.env}"

  managed_policy_arns = [aws_iam_policy.daily_collections_scheduler_policy.arn]

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "daily_collections_scheduler_policy" {
  name = "${var.service}-daily-collections-scheduler-policy-${var.env}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "sqs:SendMessage"
        Effect   = "Allow"
        Resource = aws_sqs_queue.daily_collections.arn
      },
    ]
  })
}

resource "aws_sqs_queue" "daily_collections" {
  name = "${var.service}-daily-collections-${var.env}"

  max_message_size           = 2048
  message_retention_seconds  = 600
  delay_seconds              = 0
  visibility_timeout_seconds = 30
  receive_wait_time_seconds  = 10

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.daily_collections_dlq.arn
    maxReceiveCount     = 2
  })
}

resource "aws_sqs_queue" "daily_collections_dlq" {
  name = "${var.service}-daily-collections-dlq-${var.env}"
}

resource "aws_sqs_queue_redrive_allow_policy" "daily_collections_dlq_policy" {
  queue_url = aws_sqs_queue.daily_collections_dlq.id

  redrive_allow_policy = jsonencode({
    redrivePermission = "byQueue",
    sourceQueueArns   = [aws_sqs_queue.daily_collections.arn]
  })
}
